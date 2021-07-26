__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import time
import tkinter as tk
from tkinter import ttk

import mock
import numpy as np
from PIL import Image, ImageTk

from colorization_program.src.behaviour.draw_behaviour import DrawBehaviour
from colorization_program.src.behaviour.update_behaviour import UpdateBehaviour
from colorization_program.src.colorization_algorithm.color_transfer.video.ct_async_task_video import CTAsyncTaskVideo
from colorization_program.src.colorization_algorithm.color_transfer.video.video_transfer_colorizer import \
    VideoTransferColorizer
from colorization_program.src.colorization_algorithm.colorization_using_optimization.video.cuo_async_task_video import \
    CUOAsyncTaskVideo
from colorization_program.src.colorization_algorithm.colorization_using_optimization.video.video_optimization_colorizer import \
    VideoOptimizationColorizer
from colorization_program.src.command.line_drawing_command import LineDrawingCommand
from colorization_program.src.config.pencil_config import PencilConfig
from colorization_program.src.config.singleton_config import SingletonConfig
from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver
from colorization_program.src.subject.colorization_process import ColorizationProcessSubject
from colorization_program.src.subject.colorized_image import ColorizedImageSubject
from colorization_program.src.toolkit.gui import create_info_window, create_info_confirm_window
from colorization_program.src.toolkit.image_processing import bgr_to_rgb, read_image, bgr_matrix_to_image, \
    browse_for_video, browse_for_image


class VideoDrawingCanvas(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._raw_image = None
        self._image = None
        self._video_colorizer = None
        self._video_filename = None
        self._ct_image_ref = None
        self._cuo_async_task = None
        self._waiting_indicate = None
        self._disable_drawing = False
        self._DELAY_TIME = 200
        self._state = dict()
        self._state['stop'] = []
        self._colorization_process_subject = ColorizationProcessSubject()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._show_default_image()
        self._bind_mouse_events_for_load_video()
        self._init_colorized_image_subject()
        self._colorization_process_subject.notify(start=False)

    def restore_state(self, data):
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._restore_state_cuo(data)
        else:
            self._restore_state_ct(data)

    def save_state(self):
        if SingletonConfig().colorization_algorithm == 'CUO':
            self._state['hints'] = self._draw_behaviour.save_state()
        return self._state

    def force_save_video(self):
        self._video_colorizer.force_save()

    def add_observer(self, observer):
        self._colorized_image_subject.attach(observer)

    def add_colorization_process_observer(self, observer):
        self._colorization_process_subject.attach(observer)

    def go_next(self):
        self._waiting_indicate = create_info_window("Performing colorization. Please wait...")
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._state['stop'].append(len(self._draw_behaviour.executed_commands))
            self._colorize_cuo()
        else:
            self._colorize_ct()

    def display(self, matrix):
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(matrix))
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
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CT':
            self._colorize()

    def _restore_state_ct(self, data):
        self._video_filename = data['bw']
        self._ct_image_ref = data['ref']

        window = create_info_window("Performing colorization. Please wait...")
        self._colorize_ct()
        window.destroy()

    def _restore_state_cuo(self, data):
        self._video_filename = data['bw']
        self._video_colorizer = VideoOptimizationColorizer(self._colorized_image_subject, self._video_filename)
        first_frame = self._video_colorizer.get_frame_to_colorize()

        self._init_bw_matrix(first_frame)
        self._init_pencil_config()
        self._init_draw_behaviour()
        self._init_update_behaviour()
        self._bind_mouse_events()
        self.display(bgr_to_rgb(self._matrix))
        self._push_bw_image()
        self._colorization_process_subject.notify(start=True)

        json_hints = data['hints']
        stops = np.array(data['stop'])
        self._state['stop'] = data['stop']
        counter = 0
        for hint in json_hints:
            hint_command = LineDrawingCommand.from_json(self._canvas, hint)
            hint_command.execute()
            self._draw_behaviour.executed_commands.append(hint_command)
            self._mock_click(hint)
            counter += 1
            if counter in stops:
                self._waiting_indicate = create_info_window("Performing colorization. Please wait...")
                self._restore_colorize_cuo(counter)
                while self._disable_drawing:
                    time.sleep(0.01)
                    self.update()
                    self._waiting_indicate.update()
                self._disable_drawing = True
                self._colorization_process_subject.notify(start=False)
        self._disable_drawing = False
        self._colorization_process_subject.notify(start=True)

    def _mock_click(self, hint):
        obj = mock.Mock()
        self._pencil_config.restore(hint)
        obj.x = hint['start'][0]
        obj.y = hint['start'][1]
        self._update_behaviour.on_click(obj)
        obj.x = hint['stop'][0]
        obj.y = hint['stop'][1]
        self._update_behaviour.on_click(obj)

    def _colorize_ct(self):
        self._video_colorizer = VideoTransferColorizer(self._colorized_image_subject, self._video_filename)
        first_frame = self._video_colorizer.get_first_frame()
        self._init_bw_matrix(first_frame)
        self.display(bgr_to_rgb(self._matrix))
        self._push_bw_image()

        image = read_image(self._ct_image_ref)
        self.display(bgr_to_rgb(image))
        self.update()
        self._colorization_process_subject.notify(start=False)
        self._cuo_async_task = CTAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(self._ct_image_ref)
        self.after(self._DELAY_TIME, self._check_for_ct_result)

    def _colorize_cuo(self):
        self._disable_drawing = True
        self._colorization_process_subject.notify(start=False)
        color = self._get_scribbles_matrix()
        self._cuo_async_task = CUOAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(color)
        self.after(self._DELAY_TIME, self._check_for_cuo_result)

    def _restore_colorize_cuo(self, counter):
        self._disable_drawing = True
        self._colorization_process_subject.notify(start=False)
        color = self._get_scribbles_matrix_restore(counter)
        self._cuo_async_task = CUOAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(color)
        self.after(self._DELAY_TIME, self._check_for_cuo_result)

    def _check_for_cuo_result(self):
        if self._cuo_async_task.finished:
            first_frame = self._video_colorizer.get_frame_to_colorize()
            if self._video_colorizer.video_ended:
                create_info_confirm_window("All video frames have been processed")
                if self._waiting_indicate is not None:
                    self._waiting_indicate.destroy()
                    self._disable_drawing = False
                    self._colorization_process_subject.notify(start=True)
                    return

            self._init_bw_matrix(first_frame)
            self.display(bgr_to_rgb(self._matrix))
            self._push_bw_image()

            self._waiting_indicate.destroy()
            self._disable_drawing = False
            self._colorization_process_subject.notify(start=True)
        else:
            self.after(self._DELAY_TIME, self._check_for_cuo_result)

    def _check_for_ct_result(self):
        if self._cuo_async_task.finished:
            create_info_confirm_window("All video frames have been processed")
            if self._waiting_indicate is not None:
                self._waiting_indicate.destroy()
                self._disable_drawing = False
                self._colorization_process_subject.notify(start=True)
                return
        else:
            self.after(self._DELAY_TIME, self._check_for_ct_result)

    def _colorize(self):
        window = create_info_window("Performing colorization. Please wait...")
        bw, color = self._get_colorization_input()
        x, y, result = self._update_behaviour.perform_colorize(bw, color)
        result = bgr_matrix_to_image(result)
        result = bgr_to_rgb(result)
        self._colorized_image_subject.notify(x_start=x, y_start=y, result=result)
        window.destroy()

    def _get_colorization_input(self):
        return self._matrix, self._get_scribbles_matrix()

    def _get_scribbles_matrix(self):
        index = self._get_first_command_index()
        scribbles_matrix = self._matrix.copy()
        for command in self._draw_behaviour.executed_commands[index:]:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def _get_scribbles_matrix_restore(self, counter):
        stops = self._state['stop']
        counter_idx = stops.index(counter)
        end = counter
        if counter_idx == 0:
            begin = 0
        else:
            begin = stops[counter_idx - 1]
        scribbles_matrix = self._matrix.copy()
        for command in self._draw_behaviour.executed_commands[begin:end]:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def _get_first_command_index(self):
        stops = self._state['stop']
        if stops is None or len(stops) == 1:
            return 0
        else:
            return stops[-2]

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
        self._update_behaviour = UpdateBehaviour(self._matrix, self._pencil_config.pencil_config_subject)

    def _init_draw_behaviour(self):
        self._draw_behaviour = DrawBehaviour(self._canvas, self._pencil_config.pencil_config_subject)

    def _bind_mouse_events(self):
        self._canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self._canvas.bind("<Button-1>", self.on_mouse_click)
        self._canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

    def _bind_mouse_events_for_load_video(self):
        self._canvas.bind("<Button-1>", self._load_video)

    def _load_video(self, e):
        self._video_filename = browse_for_video()
        if self._video_filename is not None:
            colorization_algorithm = SingletonConfig().colorization_algorithm
            self._state['bw'] = self._video_filename
            if colorization_algorithm == 'CUO':
                self._video_colorizer = VideoOptimizationColorizer(self._colorized_image_subject, self._video_filename)
                first_frame = self._video_colorizer.get_frame_to_colorize()
                self._init_bw_matrix(first_frame)
                self._init_pencil_config()
                self._init_draw_behaviour()
                self._init_update_behaviour()
                self._bind_mouse_events()
                self.display(bgr_to_rgb(self._matrix))
                self._push_bw_image()
                self._colorization_process_subject.notify(start=True)
            else:

                self._ct_image_ref = browse_for_image('Select reference image')
                self._state['ref'] = self._ct_image_ref
                if self._ct_image_ref is not None:
                    self._video_colorizer = VideoTransferColorizer(self._colorized_image_subject, self._video_filename)
                    first_frame = self._video_colorizer.get_first_frame()
                    self._init_bw_matrix(first_frame)
                    self.display(bgr_to_rgb(self._matrix))
                    self._push_bw_image()

                    image = read_image(self._ct_image_ref)
                    self.display(bgr_to_rgb(image))
                    self.update()

                else:
                    self._colorized_image_subject.notify(reset=True)
                    self._show_default_image()
                    return

            self._colorization_process_subject.notify(start=True)

    def _init_bw_matrix(self, matrix):
        self._matrix = matrix
        self._color_matrix = matrix.copy()

    def _show_default_image(self):
        matrix = read_image('../assets/load_video.bmp')
        self._init_canvas(matrix)
        self._init_bw_matrix(matrix)
        self.display(matrix)

    def _init_colorized_image_subject(self):
        self._colorized_image_subject = ColorizedImageSubject()

    def _push_bw_image(self):
        result = bgr_to_rgb(self._matrix)
        self._colorized_image_subject.notify(fill=True, result=result)
