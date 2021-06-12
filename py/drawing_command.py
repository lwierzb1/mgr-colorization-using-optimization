import abc
import tkinter as tk

import command


class DrawingCommand(command.Command):
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas

    @abc.abstractmethod
    def undo(self):
        pass

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def execute_on_matrix(self, matrix):
        pass
