__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

from colorization_program.src.config.consts import HEX_BLACK, RGB_BLACK
from colorization_program.src.toolkit import image_processing


class PencilColorChooser(ttk.Frame):
    def __init__(self, master, config_subject, **kw):
        super().__init__(master, **kw)
        self._color_bgr = None
        self._color_hex = None

        self._init_colors()
        self._init_config_subject(config_subject)
        self._create_color_viewer()

    def apply(self, fill_hex):
        self._color_hex = fill_hex
        self._color_bgr = image_processing.hex_to_bgr(fill_hex)
        self._display_current_color()
        self._share_colors()
        self.update()

    def add_observer(self, observer):
        self._pencil_config_subject.attach(observer)

    def _init_config_subject(self, config_subject):
        self._pencil_config_subject = config_subject

    def _init_colors(self):
        self._color_bgr = RGB_BLACK
        self._color_hex = HEX_BLACK

    def _create_color_viewer(self):
        self._frame = tk.Frame(self, width=100, height=100, background=self._color_hex)
        self._frame.place(in_=self, anchor='c', relx=0.5, rely=0.5)
        self._frame.pack()
        self._frame.bind("<Button-1>", self._pick_color)

    def _pick_color(self, event):
        colors = colorchooser.askcolor()
        self._save_colors(colors)
        self._share_colors()

    def _share_colors(self):
        self._pencil_config_subject.notify(hex=self._color_hex, bgr=self._color_bgr)

    def _save_colors(self, colors):
        self._color_bgr = colors[0]
        self._color_hex = colors[1]
        self._display_current_color()

    def _display_current_color(self):
        self._frame.config(background=self._color_hex)
