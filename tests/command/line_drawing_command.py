import tests.context
from unittest import TestCase
import tkinter as tk

from src.command.line_drawing_command import LineDrawingCommand


class LineDrawingCommandTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._canvas = tk.Canvas()
        self._command = LineDrawingCommand(self._canvas, start=(100, 100), stop=(200, 200),
                                           width=1, fill='#000000')

    def test_draw_line(self):
        self._command.execute()
        self.assertEqual(len(self._canvas.find_all()), 1)
        self._command.undo()
        self.assertEqual(len(self._canvas.find_all()), 0)
