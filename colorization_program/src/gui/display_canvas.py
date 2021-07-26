__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk
from tkinter import ttk

import PIL
import cv2
import numpy as np
from PIL import Image, ImageTk

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image import \
    image_colorizer_multiprocess
from colorization_program.src.observer.observer import Observer
from colorization_program.src.toolkit import image_processing


class DisplayCanvas(tk.ttk.Frame, Observer):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._raw_image = None
        self._image = None
        self.image_array = None
        self._canvas = None
        self._show_default_image()

    def update_color(self, bw, marked):
        colorizer = image_colorizer_multiprocess.ImageColorizerMultiprocess(bw, marked)
        result = colorizer.colorize() * 255
        result = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_BGR2RGB)
        self.display(result)

    def display(self, array):
        self.image_array = array
        self._raw_image = ImageTk.PhotoImage(image=PIL.Image.fromarray(array))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self.update()

    def update_subject(self, **kwargs):
        x_start = kwargs.get('x_start')
        y_start = kwargs.get('y_start')
        result = kwargs.get('result')
        fill = kwargs.get('fill')
        reference = kwargs.get('reference')
        reset = kwargs.get('reset')

        if reset is True:
            self._show_default_image()
            return

        if fill is True:
            self.display(result)
            self._canvas.config(height=result.shape[0])
            self._canvas.config(width=result.shape[1])
        else:
            needs_gray_detector = self._check_if_needs_gray_detection(reference, x_start, y_start)
            if needs_gray_detector:
                result = self._remove_grayscale_pixels_before_merge(result, x_start, y_start)

            height = result.shape[0]
            width = result.shape[1]
            self.image_array[y_start:y_start + height, x_start:x_start + width] = result
            self.display(self.image_array)

    def _init_canvas(self, input_matrix):
        self._image = None
        self._raw_image = None
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1], bd=0,
                                 highlightthickness=0)
        self._canvas.pack()

    def _show_default_image(self):
        matrix = image_processing.read_image('../assets/info_idle.bmp')
        if self._canvas is None:
            self._init_canvas(matrix)
        self.display(matrix)

    def _check_if_needs_gray_detection(self, reference, x_start, y_start):
        sub_array = self.image_array[y_start:y_start + reference.shape[0], x_start:x_start + reference.shape[1]]
        bgr_sub_array = cv2.cvtColor(sub_array, cv2.COLOR_RGB2BGR)
        return not np.allclose(bgr_sub_array, reference)

    def _remove_grayscale_pixels_before_merge(self, result, x_start, y_start):
        hsv = cv2.cvtColor(result, cv2.COLOR_RGB2HSV)
        lower_gray = np.array([0, 5, 10], np.uint8)
        upper_gray = np.array([179, 50, 255], np.uint8)
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
        img_res = cv2.bitwise_and(result, result, mask=mask_gray)

        was_colored = np.sum(img_res, axis=2) == 0

        for i in range(was_colored.shape[0]):
            for j in range(was_colored.shape[1]):
                if not was_colored[i, j]:
                    result[i, j] = self.image_array[y_start + i, x_start + j]
        return result
