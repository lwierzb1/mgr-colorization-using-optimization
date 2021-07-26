__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk
from tkinter import ttk


class PencilWidthPicker(ttk.Frame):
    def __init__(self, master, config_subject, **kw):
        super().__init__(master, **kw)
        self._init_default_values()
        self._init_pencil_width()
        self._create_slider()
        self._create_pencil_width_example_display()
        self._init_pencil_config_subject(config_subject)

    def apply(self, width):
        self._update_pencil_width(width)
        self._slider.set(width)
        self.update()

    def add_observer(self, observer):
        self._pencil_config_subject.attach(observer)

    def _create_slider(self):
        self._slider = ttk.Scale(self,
                                 from_=self._MIN_PENCIL_WIDTH,
                                 to=self._MAX_PENCIL_WIDTH,
                                 orient=tk.HORIZONTAL,
                                 command=self._update_pencil_width,
                                 length='100px')
        self._slider.pack()

    def _create_pencil_width_example_display(self):
        self._canvas = tk.Canvas(self,
                                 width=self._EXAMPLE_CANVAS_WIDTH,
                                 height=self._EXAMPLE_CANVAS_HEIGHT, bd=0,
                                 highlightthickness=0)
        self._canvas.pack()

    def _update_pencil_width(self, value):
        self._pencil_width = value
        self._show_pencil_width()
        self._share_pencil_width()

    def _show_pencil_width(self):
        self._canvas.delete('all')
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        self._canvas.create_line(width / 2,
                                 height / 2,
                                 width / 2,
                                 height / 2,
                                 width=self._pencil_width,
                                 fill='black',
                                 capstyle=tk.ROUND,
                                 smooth=True)

    def _share_pencil_width(self):
        self._pencil_config_subject.notify(width=self._pencil_width)

    def _init_default_values(self):
        self._MIN_PENCIL_WIDTH = 1
        self._MAX_PENCIL_WIDTH = 50
        self._EXAMPLE_CANVAS_WIDTH = 50
        self._EXAMPLE_CANVAS_HEIGHT = 50

    def _init_pencil_width(self):
        self._pencil_width = self._MIN_PENCIL_WIDTH

    def _init_pencil_config_subject(self, config_subject):
        self._pencil_config_subject = config_subject
