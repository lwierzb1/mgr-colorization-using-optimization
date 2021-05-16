from tkinter import *

from pencil_config_observer import PencilConfigObserver
from line_drawing_command import LineDrawingCommand
from pencil_config_subject import PencilConfigSubject


class DrawBehaviour:
    def __init__(self, canvas: Canvas, pencil_config_subject: PencilConfigSubject):
        self.__init_pencil_config_observer(pencil_config_subject)
        self.__canvas = canvas
        self.__old_x = None
        self.__old_y = None
        self.__history = dict()
        self.created_lines = []
        self.executed_commands = []
        self._undo_commands = []

    def save_state(self):
        return [x.get_state() for x in self.executed_commands]

    def undo_last_command(self):
        if len(self.executed_commands) > 0:
            last_command = self.executed_commands.pop()
            self.__undo_command(last_command)

    def redo_last_command(self):
        if len(self._undo_commands) > 0:
            last_command = self._undo_commands.pop()
            self.__run_command(last_command)

    def draw_dot(self, e):
        event_x = e.x
        event_y = e.y
        self.__draw_line((event_x, event_y), (event_x, event_y))
        self.__remember_position(e)

    def draw(self, e):
        event_x = e.x
        event_y = e.y
        if self.__have_old_coordinates():
            if self.__is_event_position_valid(e):
                self.__draw_line((self.__old_x, self.__old_y), (event_x, event_y))
                self.__remember_position(e)
            else:
                self.__forget_old_coordinates()

    def on_release(self, e):
        self.__forget_old_coordinates()

    def __have_old_coordinates(self):
        return self.__old_x and self.__old_y

    def __forget_old_coordinates(self):
        self.__old_y = None
        self.__old_x = None

    def __is_event_position_valid(self, e):
        width = self.__canvas.winfo_width()
        height = self.__canvas.winfo_height()
        return 0 <= e.x <= width and 0 <= e.y <= height

    def __remember_position(self, e):
        self.__old_x = e.x
        self.__old_y = e.y

    def __draw_line(self, start, stop):
        command = LineDrawingCommand(self.__canvas,
                                     start=start,
                                     stop=stop,
                                     width=self._pencil_config_observer.width,
                                     fill=self._pencil_config_observer.hex)
        self.__run_command(command)

    def __run_command(self, command):
        command.execute()
        self.executed_commands.append(command)

    def __undo_command(self, command):
        command.undo()
        self._undo_commands.append(command)

    def __init_pencil_config_observer(self, pencil_config_subject):
        self._pencil_config_observer = PencilConfigObserver()
        pencil_config_subject.attach(self._pencil_config_observer)
