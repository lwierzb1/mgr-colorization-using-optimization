from tkinter import *


class DrawBehaviour:
    def __init__(self, canvas: Canvas):
        self.pen_width = 11
        self.pen_color = 'red'
        self.__canvas = canvas
        self.__old_x = None
        self.__old_y = None
        self.created_lines = []

    def draw_dot(self, e):
        event_x = e.x
        event_y = e.y
        self.__draw_line(event_x, event_y, event_x, event_y)
        self.__remember_position(e)

    def draw(self, e):
        event_x = e.x
        event_y = e.y
        if self.__old_x and self.__old_y:
            self.__draw_line(self.__old_x, self.__old_y, event_x, event_y)

        self.__remember_position(e)

    def on_release(self, e):
        self.__old_y = None
        self.__old_x = None

    def __remember_position(self, e):
        self.__old_x = e.x
        self.__old_y = e.y

    def __draw_line(self, x_start, y_start, x_stop, y_stop):
        line = self.__canvas.create_line(x_start,
                                         y_start,
                                         x_stop,
                                         y_stop,
                                         width=self.pen_width,
                                         fill=self.pen_color,
                                         capstyle=ROUND,
                                         smooth=False)

        self.created_lines.append(line)
