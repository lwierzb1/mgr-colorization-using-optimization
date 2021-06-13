from abc import ABC
import tkinter as tk
import PIL


class AbstractCanvas(ABC):
    def __init__(self, master, matrix):
        self._master = master
        self._image = None
        self._raw_image = None
        self._frame = tk.Frame(self._master, height=matrix.shape[0], width=matrix.shape[1])
        self._frame.pack()
        self._canvas = tk.Canvas(self._frame, height=matrix.shape[0], width=matrix.shape[1])
        self._canvas.pack(fill="both", expand=True)

    def display(self, matrix):
        self._raw_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(matrix))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.pack()
