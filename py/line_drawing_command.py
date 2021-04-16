from drawing_command import DrawingCommand
import tkinter as tk
import cv2
from image_processing_toolkit import hex_to_bgr


class LineDrawingCommand(DrawingCommand):
    def __init__(self, canvas: tk.Canvas, **kwargs):
        super().__init__(canvas)
        self._line_id = None
        self._start = kwargs.get('start')
        self._stop = kwargs.get('stop')
        self._width = kwargs.get('width')
        self._fill = kwargs.get('fill')

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
        color = hex_to_bgr(self._fill)
        width = int(float(self._width))
        cv2.line(matrix, self._start, self._stop, color=color, thickness=width)
