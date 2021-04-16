import tkinter as tk


class PencilWidthPicker(tk.Frame):
    def __init__(self, master, config_subject):
        tk.Frame.__init__(self, master=master)
        self.__init_default_values()
        self.__init_pencil_width()
        self.__create_slider()
        self.__create_pencil_width_example_display()
        self.__init_pencil_config_subject(config_subject)

    def add_observer(self, observer):
        self._pencil_config_subject.attach(observer)

    def __create_slider(self):
        self._slider = tk.Scale(self,
                                from_=self.__MIN_PENCIL_WIDTH,
                                to=self.__MAX_PENCIL_WIDTH,
                                orient=tk.HORIZONTAL,
                                command=self.__update_pencil_width,
                                length='100px',
                                label='Pencil width:')
        self._slider.pack()

    def __create_pencil_width_example_display(self):
        self._canvas = tk.Canvas(self,
                                 width=self.__EXAMPLE_CANVAS_WIDTH,
                                 height=self.__EXAMPLE_CANVAS_HEIGHT)
        self._canvas.pack()

    def __update_pencil_width(self, value):
        self.__pencil_width = value
        self.__show_pencil_width()
        self.__share_pencil_width()

    def __show_pencil_width(self):
        self._canvas.delete('all')
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        self._canvas.create_line(width / 2,
                                 height / 2,
                                 width / 2,
                                 height / 2,
                                 width=self.__pencil_width,
                                 fill='black',
                                 capstyle=tk.ROUND,
                                 smooth=True)

    def __share_pencil_width(self):
        self._pencil_config_subject.notify(width=self.__pencil_width)

    def __init_default_values(self):
        self.__MIN_PENCIL_WIDTH = 1
        self.__MAX_PENCIL_WIDTH = 50
        self.__EXAMPLE_CANVAS_WIDTH = 50
        self.__EXAMPLE_CANVAS_HEIGHT = 50

    def __init_pencil_width(self):
        self.__pencil_width = self.__MIN_PENCIL_WIDTH

    def __init_pencil_config_subject(self, config_subject):
        self._pencil_config_subject = config_subject
