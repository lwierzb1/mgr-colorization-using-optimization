import tkinter as tk
from tkinter import ttk

from observer import Observer


class StyledObserverButton(ttk.Button, Observer):
    def update_subject(self, **kwargs):
        start = kwargs.get('start')
        if start:
            self.configure(state=tk.NORMAL)
        else:
            self.configure(state=tk.DISABLED)

        self.update()
