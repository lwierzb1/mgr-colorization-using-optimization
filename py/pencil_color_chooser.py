import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

import consts
import image_processing_toolkit


class PencilColorChooser(ttk.Frame):
    def __init__(self, master, config_subject, **kw):
        super().__init__(master, **kw)
        self._color_rgb = None
        self._color_hex = None

        self.__init_colors()
        self.__init_config_subject(config_subject)
        self.__create_color_viewer()

    def apply(self, fill_hex):
        self._color_hex = fill_hex
        self._color_rgb = image_processing_toolkit.hex_to_bgr(fill_hex)
        self.__display_current_color()
        self.update()

    def add_observer(self, observer):
        self._pencil_config_subject.attach(observer)

    def __init_config_subject(self, config_subject):
        self._pencil_config_subject = config_subject

    def __init_colors(self):
        self._color_rgb = consts.RGB_BLACK
        self._color_hex = consts.HEX_BLACK

    def __create_color_viewer(self):
        self.__frame = tk.Frame(self, width=100, height=100, background=self._color_hex)
        self.__frame.place(in_=self, anchor='c', relx=0.5, rely=0.5)
        self.__frame.pack()
        self.__frame.bind("<Button-1>", self.__pick_color)

    def __pick_color(self, event):
        colors = colorchooser.askcolor()
        self.__save_colors(colors)
        self.__share_colors()

    def __share_colors(self):
        self._pencil_config_subject.notify(hex=self._color_hex, rgb=self._color_rgb)

    def __save_colors(self, colors):
        self._color_rgb = colors[0]
        self._color_hex = colors[1]
        self.__display_current_color()

    def __display_current_color(self):
        self.__frame.config(background=self._color_hex)
