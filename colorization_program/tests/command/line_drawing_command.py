__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase
import tkinter as tk

from colorization_program.src.command.line_drawing_command import LineDrawingCommand


class LineDrawingCommandTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def setUp(self):
        self._canvas = tk.Canvas()
        self._command = LineDrawingCommand(self._canvas, start=(100, 100), stop=(200, 200),
                                           width=1, fill='#000000')

    def test_draw_line(self):
        self._command.execute()
        self.assertEqual(len(self._canvas.find_all()), 1)
        self._command.undo()
        self.assertEqual(len(self._canvas.find_all()), 0)
