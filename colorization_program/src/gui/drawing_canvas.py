__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import time
import tkinter as tk
from tkinter import ttk

import PIL
import mock
import numpy as np

from colorization_program.src.behaviour.draw_behaviour import DrawBehaviour
from colorization_program.src.colorization_algorithm.color_transfer.image import ct_async_task
from colorization_program.src.behaviour import update_behaviour
from colorization_program.src.command.line_drawing_command import LineDrawingCommand
from colorization_program.src.config.pencil_config import PencilConfig
from colorization_program.src.config.singleton_config import SingletonConfig
from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver
from colorization_program.src.subject.colorization_process import ColorizationProcessSubject
from colorization_program.src.subject.colorized_image import ColorizedImageSubject
from colorization_program.src.toolkit import gui, image_processing


class DrawingCanvas(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._raw_image = None
        self._image = None
        self._image_path = None
        self._in_restore = False
        self._canvas = None
        self._waiting_indicate = None
        self._disable_drawing = False
        self._ct_async_task = ct_async_task.CTAsyncTask()
        self._DELAY_TIME = 200
        self._state = dict()
        self._state['stop'] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._colorization_process_subject = ColorizationProcessSubject()
        self._show_default_image()
        self._bind_mouse_events_for_load_image()
        self._init_colorized_image_subject()
        self._colorization_process_subject.notify(start=False)

    def save_state(self):
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._state['hints'] = self._draw_behaviour.save_state()
        return self._state

    def add_observer(self, observer):
        self._colorized_image_subject.attach(observer)

    def add_colorization_process_observer(self, observer):
        self._colorization_process_subject.attach(observer)

    def display(self, matrix):
        self._raw_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(matrix))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.config(height=matrix.shape[0])
        self._canvas.config(width=matrix.shape[1])

    def undo_last_command(self, e):
        self._draw_behaviour.undo_last_command()

    def redo_last_command(self, e):
        self._draw_behaviour.redo_last_command()

    def on_mouse_motion(self, e):
        if self._disable_drawing:
            return
        self._draw_behaviour.draw(e)
        self._update_behaviour.on_motion(e)

    def on_mouse_click(self, e):
        if self._disable_drawing:
            return
        self._draw_behaviour.draw_dot(e)
        self._update_behaviour.on_click(e)

    def on_mouse_release(self, e):
        if self._disable_drawing:
            return
        self._draw_behaviour.on_release(e)
        self._state['stop'].append(len(self._draw_behaviour.executed_commands))
        self._colorize()

    def restore_state(self, data):
        self._colorization_process_subject.notify(start=False)
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._restore_state_cuo(data)
        else:
            self._restore_state_ct(data)

    def _restore_state_ct(self, data):
        self._image_path = data['bw']
        image = image_processing.read_image(self._image_path)
        self._init_bw_matrix(image)
        self.display(image_processing.bgr_to_rgb(self._matrix))
        self._push_bw_image()

        self._image_path = data['ref']
        image = image_processing.read_image(self._image_path)
        self._init_bw_matrix(image)
        self.display(image_processing.bgr_to_rgb(self._matrix))

        self._colorize_ct(image_processing.read_image(data['ref']),
                          image_processing.read_image(data['bw']))

    def _restore_state_cuo(self, data):
        self._image_path = data['bw']
        image = image_processing.read_image(self._image_path)
        self._init_bw_matrix(image)
        self._init_pencil_config()
        self._init_draw_behaviour()
        self._init_update_behaviour()
        self._bind_mouse_events()
        self.display(image_processing.bgr_to_rgb(self._matrix))
        self._push_bw_image()
        json_hints = data['hints']
        stops = np.array(data['stop'])
        counter = 0
        for hint in json_hints:
            hint_command = LineDrawingCommand.from_json(self._canvas, hint)
            hint_command.execute()
            self._draw_behaviour.executed_commands.append(hint_command)
            self._mock_click(hint)
            counter += 1
            if counter in stops:
                self._colorize()
                while self._disable_drawing:
                    time.sleep(0.01)
                    self.update()
                    self._waiting_indicate.update()
                self._disable_drawing = True
                self._colorization_process_subject.notify(start=False)
        self._state['bw'] = data['bw']
        self._state['stop'] = data['stop']
        self._colorization_process_subject.notify(start=True)
        self._disable_drawing = False

    def _mock_click(self, hint):
        obj = mock.Mock()
        self._pencil_config.restore(hint)
        obj.x = hint['start'][0]
        obj.y = hint['start'][1]
        self._update_behaviour.on_click(obj)
        obj.x = hint['stop'][0]
        obj.y = hint['stop'][1]
        self._update_behaviour.on_click(obj)

    def _colorize(self):
        self._disable_drawing = True
        self._waiting_indicate = gui.create_info_window("Performing colorization. Please wait...")
        bw, color = self._get_colorization_input()
        self._update_behaviour.perform_colorize(bw, color)
        self.after(self._DELAY_TIME, self._check_for_cuo_result)

    def _check_for_cuo_result(self):
        result_candidate = self._update_behaviour.check_for_result()
        if result_candidate is not None:
            x = result_candidate[0]
            y = result_candidate[1]
            result = result_candidate[2]
            result = image_processing.bgr_matrix_to_image(result)
            result = image_processing.bgr_to_rgb(result)

            bw, _ = self._get_colorization_input()
            self._colorized_image_subject.notify(x_start=x, y_start=y, result=result,
                                                 reference=bw[y:y + result.shape[0], x:x + result.shape[1]])

            self._waiting_indicate.destroy()
            self._disable_drawing = False
        else:
            self.after(self._DELAY_TIME, self._check_for_cuo_result)

    def _check_for_ct_result(self):
        result_candidate = self._ct_async_task.result()
        if result_candidate is not None:
            result = image_processing.bgr_to_rgb(result_candidate)
            self._colorized_image_subject.notify(x_start=0, y_start=0, result=result, fill=True)
            self._colorization_process_subject.notify(start=True)

            self._waiting_indicate.destroy()
            self._disable_drawing = False
        else:
            self.after(self._DELAY_TIME, self._check_for_ct_result)

    def _get_colorization_input(self):
        return self._matrix, self._get_scribbles_matrix()

    def _get_scribbles_matrix(self):
        scribbles_matrix = self._matrix.copy()
        for command in self._draw_behaviour.executed_commands:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def _init_canvas(self, input_matrix):
        self._image = None
        self._raw_image = None
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1], bd=0,
                                 highlightthickness=0)
        self._canvas.pack(side=tk.RIGHT)

    def _init_pencil_config(self):
        self._pencil_config_observer = PencilConfigObserver()
        self._pencil_config = PencilConfig(self)
        self._pencil_config.pencil_config_subject.attach(self._pencil_config_observer)
        self._pencil_config.pack(side=tk.LEFT, padx=20)

    def _init_update_behaviour(self):
        self._update_behaviour = update_behaviour.UpdateBehaviour(self._matrix,
                                                                  self._pencil_config.pencil_config_subject)

    def _init_draw_behaviour(self):
        self._draw_behaviour = DrawBehaviour(self._canvas, self._pencil_config.pencil_config_subject)

    def _bind_mouse_events(self):
        self._canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self._canvas.bind("<Button-1>", self.on_mouse_click)
        self._canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

    def _bind_mouse_events_for_load_image(self):
        self._canvas.bind("<Button-1>", self._load_image)

    def _load_image(self, e):
        if self._disable_drawing:
            return

        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._image_path = image_processing.browse_for_image('Select image to colorize')
            self._state['bw'] = self._image_path
            if self._image_path is not None:
                image = image_processing.read_image(self._image_path)
                self._init_bw_matrix(image)
                self._init_pencil_config()
                self._init_draw_behaviour()
                self._init_update_behaviour()
                self._bind_mouse_events()
                self.display(image_processing.bgr_to_rgb(self._matrix))
                self._push_bw_image()
            else:
                self._show_default_image()
                return
            self._colorization_process_subject.notify(start=True)
        else:
            self._image_path = image_processing.browse_for_image('Select image to colorize')
            self._state['bw'] = self._image_path
            if self._image_path is not None:
                image = image_processing.read_image(self._image_path)
                self._init_bw_matrix(image)
                self.display(image_processing.bgr_to_rgb(self._matrix))
                self._push_bw_image()
            else:
                self._show_default_image()
                return

            self._image_path = image_processing.browse_for_image('Select reference image')
            self._state['ref'] = self._image_path
            if self._image_path is not None:
                image = image_processing.read_image(self._image_path)
                self._init_bw_matrix(image)
                self.display(image_processing.bgr_to_rgb(image))
                self.update()
            else:
                self._colorized_image_subject.notify(reset=True)
                self._show_default_image()
                return
            self._colorize_ct(image_processing.read_image(self._state['ref']),
                              image_processing.read_image(self._state['bw']))

    def _colorize_ct(self, ref, bw):
        self._colorization_process_subject.notify(start=False)
        self._disable_drawing = True
        self._waiting_indicate = gui.create_info_window("Performing colorization. Please wait...")
        self._ct_async_task.run(ref, bw)
        self.after(self._DELAY_TIME, self._check_for_ct_result)

    def _init_bw_matrix(self, matrix):
        self._matrix = matrix
        self._color_matrix = matrix.copy()

    def _show_default_image(self):
        matrix = image_processing.read_image('../assets/info_load.bmp')
        if self._canvas is None:
            self._init_canvas(matrix)
        self._init_bw_matrix(matrix)
        self.display(matrix)

    def _init_colorized_image_subject(self):
        self._colorized_image_subject = ColorizedImageSubject()

    def _push_bw_image(self):
        result = image_processing.bgr_to_rgb(self._matrix)
        self._colorized_image_subject.notify(x_start=0, y_start=0, result=result, fill=True)
