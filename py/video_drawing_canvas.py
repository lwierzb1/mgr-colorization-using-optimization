import time
import tkinter as tk
from tkinter import ttk

import mock
import numpy as np
from PIL import Image, ImageTk

from colorization_process_subject import ColorizationProcessSubject
from colorized_image_subject import ColorizedImageSubject
from cuo_async_task_video import CUOAsyncTaskVideo
from draw_behaviour import DrawBehaviour
from gui_toolkit import create_info_window, create_info_confirm_window
from image_processing_toolkit import bgr_to_rgb, read_image, bgr_matrix_to_image, browse_for_video, browse_for_image
from line_drawing_command import LineDrawingCommand
from pencil_config import PencilConfig
from pencil_config_observer import PencilConfigObserver
from py.ct_async_task_video import CTAsyncTaskVideo
from singleton_config import SingletonConfig
from update_behaviour import UpdateBehaviour
from video_optimization_colorizer import VideoOptimizationColorizer
from video_transfer_colorizer import VideoTransferColorizer


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
        self.__DELAY_TIME = 200
        self._state = dict()
        self._state['stop'] = []
        self._colorization_process_subject = ColorizationProcessSubject()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.__show_default_image()
        self.__bind_mouse_events_for_load_video()
        self.__init_colorized_image_subject()
        self._colorization_process_subject.notify(start=False)

    def restore_state(self, data):
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._restore_state_cuo(data)
        else:
            self._restore_state_ct(data)

    def _restore_state_ct(self, data):
        self._video_filename = data['bw']
        self._ct_image_ref = data['ref']

        window = create_info_window("Performing colorization. Please wait...")
        self._colorize_ct()
        window.destroy()

    def _restore_state_cuo(self, data):
        self._video_filename = data['bw']
        self._video_colorizer = VideoOptimizationColorizer(self.__colorized_image_subject, self._video_filename)
        first_frame = self._video_colorizer.get_frame_to_colorize()

        self.__init_bw_matrix(first_frame)
        self.__init_pencil_config()
        self.__init_draw_behaviour()
        self.__init_update_behaviour()
        self.__bind_mouse_events()
        self.display(bgr_to_rgb(self.__matrix))
        self.__push_bw_image()
        self._colorization_process_subject.notify(start=True)

        json_hints = data['hints']
        stops = np.array(data['stop'])
        self._state['stop'] = data['stop']
        counter = 0
        for hint in json_hints:
            hint_command = LineDrawingCommand.from_json(self._canvas, hint)
            hint_command.execute()
            self.__draw_behaviour.executed_commands.append(hint_command)
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
        self.__update_behaviour.on_click(obj)
        obj.x = hint['stop'][0]
        obj.y = hint['stop'][1]
        self.__update_behaviour.on_click(obj)

    def save_state(self):
        if SingletonConfig().colorization_algorithm == 'CUO':
            self._state['hints'] = self.__draw_behaviour.save_state()
        return self._state

    def force_save_video(self):
        self._video_colorizer.force_save()

    def add_observer(self, observer):
        self.__colorized_image_subject.attach(observer)

    def add_colorization_process_observer(self, observer):
        self._colorization_process_subject.attach(observer)

    def go_next(self):
        self._waiting_indicate = create_info_window("Performing colorization. Please wait...")
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._state['stop'].append(len(self.__draw_behaviour.executed_commands))
            self._colorize_cuo()
        else:
            self._colorize_ct()

    def _colorize_ct(self):
        self._video_colorizer = VideoTransferColorizer(self.__colorized_image_subject, self._video_filename)
        first_frame = self._video_colorizer.get_first_frame()
        self.__init_bw_matrix(first_frame)
        self.display(bgr_to_rgb(self.__matrix))
        self.__push_bw_image()

        image = read_image(self._ct_image_ref)
        self.display(bgr_to_rgb(image))
        self.update()
        self._colorization_process_subject.notify(start=False)
        self._cuo_async_task = CTAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(self._ct_image_ref)
        self.after(self.__DELAY_TIME, self._check_for_ct_result)

    def _colorize_cuo(self):
        self._disable_drawing = True
        self._colorization_process_subject.notify(start=False)
        color = self.__get_scribbles_matrix()
        self._cuo_async_task = CUOAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(color)
        self.after(self.__DELAY_TIME, self._check_for_cuo_result)

    def _restore_colorize_cuo(self, counter):
        self._disable_drawing = True
        self._colorization_process_subject.notify(start=False)
        color = self.__get_scribbles_matrix_restore(counter)
        self._cuo_async_task = CUOAsyncTaskVideo(self._video_colorizer)
        self._cuo_async_task.run(color)
        self.after(self.__DELAY_TIME, self._check_for_cuo_result)

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

            self.__init_bw_matrix(first_frame)
            self.display(bgr_to_rgb(self.__matrix))
            self.__push_bw_image()

            self._waiting_indicate.destroy()
            self._disable_drawing = False
            self._colorization_process_subject.notify(start=True)
        else:
            self.after(self.__DELAY_TIME, self._check_for_cuo_result)

    def _check_for_ct_result(self):
        if self._cuo_async_task.finished:
            create_info_confirm_window("All video frames have been processed")
            if self._waiting_indicate is not None:
                self._waiting_indicate.destroy()
                self._disable_drawing = False
                self._colorization_process_subject.notify(start=True)
                return
        else:
            self.after(self.__DELAY_TIME, self._check_for_ct_result)

    def display(self, matrix):
        self._raw_image = ImageTk.PhotoImage(image=Image.fromarray(matrix))
        self._image = self._canvas.create_image(0, 0, image=self._raw_image, anchor="nw")
        self._canvas.config(height=matrix.shape[0])
        self._canvas.config(width=matrix.shape[1])

    def undo_last_command(self, e):
        self.__draw_behaviour.undo_last_command()

    def redo_last_command(self, e):
        self.__draw_behaviour.redo_last_command()

    def on_mouse_motion(self, e):
        if self._disable_drawing:
            return
        self.__draw_behaviour.draw(e)
        self.__update_behaviour.on_motion(e)

    def on_mouse_click(self, e):
        if self._disable_drawing:
            return
        self.__draw_behaviour.draw_dot(e)
        self.__update_behaviour.on_click(e)

    def on_mouse_release(self, e):
        if self._disable_drawing:
            return
        self.__draw_behaviour.on_release(e)
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CT':
            self.__colorize()

    def __colorize(self):
        window = create_info_window("Performing colorization. Please wait...")
        bw, color = self.__get_colorization_input()
        x, y, result = self.__update_behaviour.perform_colorize(bw, color)
        result = bgr_matrix_to_image(result)
        result = bgr_to_rgb(result)
        self.__colorized_image_subject.notify(x_start=x, y_start=y, result=result)
        window.destroy()

    def __get_colorization_input(self):
        return self.__matrix, self.__get_scribbles_matrix()

    def __get_scribbles_matrix(self):
        index = self.__get_first_command_index()
        scribbles_matrix = self.__matrix.copy()
        for command in self.__draw_behaviour.executed_commands[index:]:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def __get_scribbles_matrix_restore(self, counter):
        stops = self._state['stop']
        counter_idx = stops.index(counter)
        end = counter
        if counter_idx == 0:
            begin = 0
        else:
            begin = stops[counter_idx - 1]
        scribbles_matrix = self.__matrix.copy()
        for command in self.__draw_behaviour.executed_commands[begin:end]:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def __get_first_command_index(self):
        stops = self._state['stop']
        if stops is None or len(stops) == 1:
            return 0
        else:
            return stops[-2]

    def __init_canvas(self, input_matrix):
        self._image = None
        self._raw_image = None
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1], bd=0,
                                 highlightthickness=0)
        self._canvas.pack(side=tk.RIGHT)

    def __init_pencil_config(self):
        self._pencil_config_observer = PencilConfigObserver()
        self._pencil_config = PencilConfig(self)
        self._pencil_config.pencil_config_subject.attach(self._pencil_config_observer)
        self._pencil_config.pack(side=tk.LEFT, padx=20)

    def __init_update_behaviour(self):
        self.__update_behaviour = UpdateBehaviour(self.__matrix, self._pencil_config.pencil_config_subject)

    def __init_draw_behaviour(self):
        self.__draw_behaviour = DrawBehaviour(self._canvas, self._pencil_config.pencil_config_subject)

    def __bind_mouse_events(self):
        self._canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self._canvas.bind("<Button-1>", self.on_mouse_click)
        self._canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

    def __bind_mouse_events_for_load_video(self):
        self._canvas.bind("<Button-1>", self.__load_video)

    def __load_video(self, e):
        self._video_filename = browse_for_video()
        if self._video_filename is not None:
            colorization_algorithm = SingletonConfig().colorization_algorithm
            self._state['bw'] = self._video_filename
            if colorization_algorithm == 'CUO':
                self._video_colorizer = VideoOptimizationColorizer(self.__colorized_image_subject, self._video_filename)
                first_frame = self._video_colorizer.get_frame_to_colorize()
                self.__init_bw_matrix(first_frame)
                self.__init_pencil_config()
                self.__init_draw_behaviour()
                self.__init_update_behaviour()
                self.__bind_mouse_events()
                self.display(bgr_to_rgb(self.__matrix))
                self.__push_bw_image()
                self._colorization_process_subject.notify(start=True)
            else:

                self._ct_image_ref = browse_for_image('Select reference image')
                self._state['ref'] = self._ct_image_ref
                if self._ct_image_ref is not None:
                    self._video_colorizer = VideoTransferColorizer(self.__colorized_image_subject, self._video_filename)
                    first_frame = self._video_colorizer.get_first_frame()
                    self.__init_bw_matrix(first_frame)
                    self.display(bgr_to_rgb(self.__matrix))
                    self.__push_bw_image()

                    image = read_image(self._ct_image_ref)
                    self.display(bgr_to_rgb(image))
                    self.update()

                else:
                    self.__colorized_image_subject.notify(reset=True)
                    self.__show_default_image()
                    return

            self._colorization_process_subject.notify(start=True)

    def __init_bw_matrix(self, matrix):
        self.__matrix = matrix
        self.__color_matrix = matrix.copy()

    def __show_default_image(self):
        matrix = read_image('../assets/load_video.bmp')
        self.__init_canvas(matrix)
        self.__init_bw_matrix(matrix)
        self.display(matrix)

    def __init_colorized_image_subject(self):
        self.__colorized_image_subject = ColorizedImageSubject()

    def __push_bw_image(self):
        result = bgr_to_rgb(self.__matrix)
        self.__colorized_image_subject.notify(fill=True, result=result)
