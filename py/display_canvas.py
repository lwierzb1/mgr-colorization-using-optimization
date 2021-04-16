import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk

from image_colorizer_multiprocess import ImageColorizerMultiprocess
from image_processing_toolkit import read_image


class DisplayCanvas(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._raw_image = None
        self._image = None

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
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(array))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.pack()

    def __show_default_image(self):
        matrix = read_image('../assets/info_load.bmp')
        self.__init_canvas(matrix)
        self.display(matrix)
