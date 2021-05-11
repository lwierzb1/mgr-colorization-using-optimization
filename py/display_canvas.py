import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk

from image_colorizer_multiprocess import ImageColorizerMultiprocess
from image_processing_toolkit import read_image
from py.observer import Observer


class DisplayCanvas(tk.LabelFrame, Observer):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)
        self.config(text='RESULT')
        self._raw_image = None
        self._image = None
        self._image_array = None
        self.__show_default_image()

    def update_color(self, bw, marked):
        colorizer = ImageColorizerMultiprocess(bw, marked)
        result = colorizer.colorize() * 255
        result = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_BGR2RGB)
        self.display(result)

    def __init_canvas(self, input_matrix):
        self._image = None
        self._raw_image = None
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1])
        self._canvas.pack()

    def display(self, array):
        self._image_array = array
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(array))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self.update()

    def __show_default_image(self):
        matrix = read_image('../assets/info_idle.bmp')
        self.__init_canvas(matrix)
        self.display(matrix)

    def update_subject(self, **kwargs):
        x_start = kwargs.get('x_start')
        y_start = kwargs.get('y_start')
        result = kwargs.get('result')
        fill = kwargs.get('fill')
        height = result.shape[0]
        width = result.shape[1]
        if fill is True:
            self.display(result)
            self._canvas.config(height=result.shape[0])
            self._canvas.config(width=result.shape[1])
        else:
            array = self._image_array.copy()
            array[y_start:y_start + height, x_start:x_start + width] = result
            self.display(array)

    def get_result(self):
        return self._image_array
