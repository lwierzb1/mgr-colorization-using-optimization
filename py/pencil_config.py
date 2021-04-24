import tkinter as tk
from pencil_config_subject import PencilConfigSubject

from pencil_color_chooser import PencilColorChooser
from pencil_width_picker import PencilWidthPicker
from observer import Observer


class PencilConfig(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master)
        self.__create_pencil_config_subject()
        self.__create_pencil_color_chooser()
        self.__create_pencil_width_chooser()
        self.config(text='Pencil config')

    def add_observer(self, observer: Observer):
        self._color_picker.add_observer(observer)
        self._pencil_width_picker.add_observer(observer)

    def __create_pencil_color_chooser(self):
        self._color_picker = PencilColorChooser(self, self.pencil_config_subject)
        self._color_picker.pack(side=tk.TOP, padx=10, pady=10)

    def __create_pencil_width_chooser(self):
        self._pencil_width_picker = PencilWidthPicker(self, self.pencil_config_subject)
        self._pencil_width_picker.pack(side=tk.BOTTOM, padx=10, pady=10)

    def __create_pencil_config_subject(self):
        self.pencil_config_subject = PencilConfigSubject()
