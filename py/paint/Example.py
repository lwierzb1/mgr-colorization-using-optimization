from tkinter import *


class Example(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = Label(self, text="aaa", anchor="w")
        self.label.pack()
