import abc
import tkinter as tk

from py.command.command import Command


class DrawingCommand(Command):
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
