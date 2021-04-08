from abc import abstractmethod, ABC
from tkinter import Frame, Canvas

from PIL import Image, ImageTk


class AbstractDisplayCanvas(ABC):
    def __init__(self, master, matrices):
        self._master = master
        self._frame = Frame(self._master, height=960, width=720)
        self._frame.pack()

        for i in range(len(matrices)):
            for j in range(len(matrices[i])):
                self._display((i, j), matrices[i][j])
        a = 1

    @abstractmethod
    def update(self, coordinates, array):
        pass

    def _display(self, coordinate, array):
        self._raw_images[coordinate] = ImageTk.PhotoImage(image=Image.fromarray(array))
        self._images[coordinate] = self._canvases[coordinate].create_image(0, 0, image=self._raw_images[coordinate],
                                                                           anchor="nw")
        self._canvases[coordinate].grid(row=coordinate[1], column=coordinate[0])

    def __init_dictionaries(self, matrices):
        for c in range(len(matrices)):
            for r in range(len(matrices[c])):
                self._canvases[(c, r)] = Canvas(self._frame,
                                                bd=-2,
                                                height=matrices[c][r].shape[0],
                                                width=matrices[c][r].shape[1])
