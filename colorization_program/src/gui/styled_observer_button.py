__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk
from tkinter import ttk

from colorization_program.src.observer.observer import Observer


class StyledObserverButton(ttk.Button, Observer):
    def update_subject(self, **kwargs):
        start = kwargs.get('start')
        if start:
            self.configure(state=tk.NORMAL)
        else:
            self.configure(state=tk.DISABLED)

        self.update()
