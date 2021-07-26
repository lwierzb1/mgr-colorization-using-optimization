__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import abc
import tkinter as tk

from colorization_program.src.command.command import Command


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
