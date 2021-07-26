__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk

from colorization_program.src.command import line_drawing_command
from colorization_program.src.observer import pencil_config_observer
from colorization_program.src.subject import pencil_config


class DrawBehaviour:
    def __init__(self, canvas: tk.Canvas, pencil_config_subject: pencil_config.PencilConfigSubject):
        self._init_pencil_config_observer(pencil_config_subject)
        self._canvas = canvas
        self._old_x = None
        self._old_y = None
        self._history = dict()
        self.executed_commands = []
        self._undo_commands = []

    def save_state(self):
        return [x.get_state() for x in self.executed_commands]

    def undo_last_command(self):
        if len(self.executed_commands) > 0:
            last_command = self.executed_commands.pop()
            self._undo_command(last_command)

    def redo_last_command(self):
        if len(self._undo_commands) > 0:
            last_command = self._undo_commands.pop()
            self._run_command(last_command)

    def draw_dot(self, e):
        event_x = e.x
        event_y = e.y
        self._draw_line((event_x, event_y), (event_x, event_y))
        self._remember_position(e)

    def draw(self, e):
        event_x = e.x
        event_y = e.y
        if self._have_old_coordinates():
            if self._is_event_position_valid(e):
                self._draw_line((self._old_x, self._old_y), (event_x, event_y))
                self._remember_position(e)
            else:
                self._forget_old_coordinates()

    def on_release(self, e):
        self._forget_old_coordinates()

    def _have_old_coordinates(self):
        return self._old_x and self._old_y

    def _forget_old_coordinates(self):
        self._old_y = None
        self._old_x = None

    def _is_event_position_valid(self, e):
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        return 0 <= e.x <= width and 0 <= e.y <= height

    def _remember_position(self, e):
        self._old_x = e.x
        self._old_y = e.y

    def _draw_line(self, start, stop):
        command = line_drawing_command.LineDrawingCommand(self._canvas,
                                                          start=start,
                                                          stop=stop,
                                                          width=self._pencil_config_observer.width,
                                                          fill=self._pencil_config_observer.hex)
        self._run_command(command)

    def _run_command(self, command):
        command.execute()
        self.executed_commands.append(command)

    def _undo_command(self, command):
        command.undo()
        self._undo_commands.append(command)

    def _init_pencil_config_observer(self, pencil_config_subject):
        self._pencil_config_observer = pencil_config_observer.PencilConfigObserver()
        pencil_config_subject.attach(self._pencil_config_observer)
