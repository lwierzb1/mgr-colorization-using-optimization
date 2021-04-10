from abc import abstractmethod, ABC
from tkinter import Frame, Canvas, Event

from PIL import Image, ImageTk


class AbstractDrawingCanvas(ABC):
    def __init__(self, master, matrix):
        self._master = master
        self._image = None
        self._raw_image = None
        self._frame = Frame(self._master, height=matrix.shape[0], width=matrix.shape[1])
        self._frame.pack()
        self._canvas = Canvas(self._frame, height=matrix.shape[0], width=matrix.shape[1])
        self._canvas.pack(fill="both", expand=True)



    @abstractmethod
    def draw(self, e: Event):
        pass

    @abstractmethod
    def draw_dot(self, e: Event):
        pass

    @abstractmethod
    def on_release(self, e: Event):
        pass

    def __bind_draw_events(self):
        self._canvas.bind('<B1-Motion>', self.draw)
        self._canvas.bind("<Button-1>", self.draw_dot)
        self._canvas.bind('<ButtonRelease-1>', self.on_release)
