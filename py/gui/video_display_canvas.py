import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

from py.colorization_algorithm.colorization_using_optimization.image.image_colorizer_multiprocess import \
    ImageColorizerMultiprocess
from py.toolkit.image_processing import read_image
from py.observer.observer import Observer


class VideoDisplayCanvas(ttk.Frame, Observer):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
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
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1], bd=0,
                                 highlightthickness=0)
        self._canvas.pack()

    def display(self, array):
        self._image_array = array
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(array))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.config(height=array.shape[0])
        self._canvas.config(width=array.shape[1])
        self.update()

    def __show_default_image(self):
        matrix = read_image('../../assets/info_idle.bmp')
        self.__init_canvas(matrix)
        self.display(matrix)

    def update_subject(self, **kwargs):
        result = kwargs.get('result')
        self.display(result)

    def get_result(self):
        return self._image_array
