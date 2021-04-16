from abc import abstractmethod

from command import Command
import tkinter as tk


class DrawingCommand(Command):
    def __init__(self, canvas: tk.Canvas):
        self._canvas = canvas

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def execute_on_matrix(self, matrix):
        pass
