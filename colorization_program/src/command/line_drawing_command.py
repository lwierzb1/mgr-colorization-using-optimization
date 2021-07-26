__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk

import cv2

from colorization_program.src.command.drawing_command import DrawingCommand
from colorization_program.src.toolkit import image_processing


class LineDrawingCommand(DrawingCommand):
    def __init__(self, canvas: tk.Canvas, **kwargs):
        super().__init__(canvas)
        self._line_id = None
        self._start = kwargs.get('start')
        self._stop = kwargs.get('stop')
        self._width = kwargs.get('width')
        self._fill = kwargs.get('fill')

    @classmethod
    def from_json(cls, canvas, json):
        return cls(canvas, start=tuple(json['start']), stop=tuple(json['stop']), width=json['width'], fill=json['fill'])

    def get_state(self):
        state = dict()
        state['start'] = self._start
        state['stop'] = self._stop
        state['width'] = self._width
        state['fill'] = self._fill
        return state

    def undo(self):
        self._canvas.delete(self._line_id)

    def execute(self):
        self._line_id = self._canvas.create_line(self._start[0],
                                                 self._start[1],
                                                 self._stop[0],
                                                 self._stop[1],
                                                 width=self._width,
                                                 fill=self._fill,
                                                 capstyle=tk.ROUND,
                                                 smooth=False)

    def execute_on_matrix(self, matrix):
        color = image_processing.hex_to_bgr(self._fill)
        width = int(float(self._width))
        cv2.line(matrix, self._start, self._stop, color=color, thickness=width)
