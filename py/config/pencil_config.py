import tkinter as tk
from tkinter import ttk
from py.subject.pencil_config import PencilConfigSubject

from py.gui.pencil_color_chooser import PencilColorChooser
from py.gui.pencil_width_picker import PencilWidthPicker
from py.observer.observer import Observer


class PencilConfig(ttk.LabelFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._create_pencil_config_subject()
        self._create_pencil_color_chooser()
        self._create_pencil_width_chooser()

    def restore(self, data):
        self._pencil_width_picker.apply(data['width'])
        self._color_picker.apply(data['fill'])

    def add_observer(self, observer: Observer):
        self._color_picker.add_observer(observer)
        self._pencil_width_picker.add_observer(observer)

    def _create_pencil_color_chooser(self):
        self._color_picker = PencilColorChooser(self, self.pencil_config_subject)
        self._color_picker.pack(side=tk.TOP, padx=10, pady=10)

    def _create_pencil_width_chooser(self):
        self._pencil_width_picker = PencilWidthPicker(self, self.pencil_config_subject)
        self._pencil_width_picker.pack(side=tk.BOTTOM, padx=10, pady=10)

    def _create_pencil_config_subject(self):
        self.pencil_config_subject = PencilConfigSubject()
