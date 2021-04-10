import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from image_colorizer_multiprocess import ImageColorizerMultiprocess
import cv2


class DisplayCanvas(tk.Frame):
    def __init__(self, master, matrices):
        tk.Frame.__init__(self, master, height=960, width=720)
        self.pack()

        self._raw_images = dict()
        self._images = dict()
        self._canvases = dict()
        self.__init_dictionaries(matrices)

        for i in range(len(matrices)):
            for j in range(len(matrices[i])):
                self._display((i, j), matrices[i][j])

    def update_color(self, coordinates, bw, marked):
        cv2.imshow('', bw)
        cv2.waitKey(0)
        cv2.imshow('', marked)
        cv2.waitKey(0)

        colorizer = ImageColorizerMultiprocess(bw, marked)

        result = colorizer.colorize() * 255

        result = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_BGR2RGB)

        self._display(coordinates, result)

    def _display(self, coordinate, array):
        self._raw_images[coordinate] = ImageTk.PhotoImage(image=Image.fromarray(array))
        self._images[coordinate] = self._canvases[coordinate].create_image(0, 0, image=self._raw_images[coordinate],
                                                                           anchor="nw")
        self._canvases[coordinate].grid(row=coordinate[1], column=coordinate[0])

    def __init_dictionaries(self, matrices):
        for c in range(len(matrices)):
            for r in range(len(matrices[c])):
                self._canvases[(c, r)] = tk.Canvas(self,
                                                   bd=-2,
                                                   height=matrices[c][r].shape[0],
                                                   width=matrices[c][r].shape[1])
