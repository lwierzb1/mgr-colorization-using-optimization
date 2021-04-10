import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk
from PIL import ImageGrab

from draw_behaviour import DrawBehaviour
from update_behaviour import UpdateBehaviour


class DrawingCanvas(tk.Frame):
    def __init__(self, master, matrix, xd):
        tk.Frame.__init__(self, master)
        self._image = None
        self.__matrix = None
        self._raw_image = None
        self.xd = xd
        self._canvas = tk.Canvas(self, height=matrix.shape[0], width=matrix.shape[1], bd=-2)
        self._canvas.pack(fill="both", expand=True)

        self.display(matrix)
        self.__init_draw_behaviour()
        self.__init_update_behaviour(matrix)
        self.__bind_draw_events()

    def display(self, matrix):
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(matrix))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.pack()

    def draw(self, e):
        self.__draw_behaviour.draw(e)
        self.__update_behaviour.analyze(e)

    def draw_dot(self, e):
        if self.__matrix is None:
            self.__matrix = self.__get_canvas_data()
        self.__draw_behaviour.draw_dot(e)
        self.__update_behaviour.analyze(e)

    def on_release(self, e):
        self.__draw_behaviour.on_release(e)
        self.__update_canvas()
        self.__update_behaviour.clear()

    def __update_canvas(self):
        canvas_arrays = self.__get_canvas_arrays()
        aa = self.__split_array(self.__matrix)
        for coordinate in self.__update_behaviour.canvas_coordinates_to_update:
            image = canvas_arrays[coordinate[0]][coordinate[1]]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            b = cv2.cvtColor(aa[coordinate[0]][coordinate[1]], cv2.COLOR_RGB2BGR)
            cv2.imshow('', image)
            cv2.waitKey(0)
            self.xd.update_color(coordinate, b, image)

    def __get_canvas_arrays(self):
        array = self.__get_canvas_data()
        return self.__split_array(array)

    @staticmethod
    def __split_array(array):
        arrays = np.array_split(array, 2, axis=1)
        for i in range(len(arrays)):
            arrays[i] = np.array_split(arrays[i], 4, axis=0)
        return arrays

    def __get_canvas_data(self):
        x = self._canvas.winfo_rootx() + self._canvas.winfo_x()
        y = self._canvas.winfo_rooty() + self._canvas.winfo_y()
        x1 = x + self._canvas.winfo_width()
        y1 = y + self._canvas.winfo_height()
        canvas_image = ImageGrab.grab(bbox=(x, y, x1, y1))
        return np.array(canvas_image.getdata(), dtype='uint8').reshape((canvas_image.size[1], canvas_image.size[0], 3))

    def __init_update_behaviour(self, matrix):
        self.__update_behaviour = UpdateBehaviour(matrix.shape[1], matrix.shape[0])

    def __init_draw_behaviour(self):
        self.__draw_behaviour = DrawBehaviour(self._canvas)

    def __bind_draw_events(self):
        self._canvas.bind('<B1-Motion>', self.draw)
        self._canvas.bind("<Button-1>", self.draw_dot)
        self._canvas.bind('<ButtonRelease-1>', self.on_release)
