import time
import tkinter as tk
from tkinter import ttk

import PIL
import mock
import numpy as np

import colorization_process_subject
import colorized_image_subject
import ct_async_task
import draw_behaviour
import gui_toolkit
import image_processing_toolkit
import line_drawing_command
import pencil_config
import pencil_config_observer
import singleton_config
import update_behaviour


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
        self.__DELAY_TIME = 200
        self._state = dict()
        self._state['stop'] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._colorization_process_subject = colorization_process_subject.ColorizationProcessSubject()
        self.__show_default_image()
        self.__bind_mouse_events_for_load_image()
        self.__init_colorized_image_subject()
        self._colorization_process_subject.notify(start=False)

    def restore_state(self, data):
        self._colorization_process_subject.notify(start=False)
        colorization_algorithm = singleton_config.SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._restore_state_cuo(data)
        else:
            self._restore_state_ct(data)

    def _restore_state_ct(self, data):
        self._image_path = data['bw']
        image = image_processing_toolkit.read_image(self._image_path)
        self.__init_bw_matrix(image)
        self.display(image_processing_toolkit.bgr_to_rgb(self.__matrix))
        self.__push_bw_image()

        self._image_path = data['ref']
        image = image_processing_toolkit.read_image(self._image_path)
        self.__init_bw_matrix(image)
        self.display(image_processing_toolkit.bgr_to_rgb(self.__matrix))

        self.__colorize_ct(image_processing_toolkit.read_image(data['ref']),
                           image_processing_toolkit.read_image(data['bw']))

    def _restore_state_cuo(self, data):
        self._image_path = data['bw']
        image = image_processing_toolkit.read_image(self._image_path)
        self.__init_bw_matrix(image)
        self.__init_pencil_config()
        self.__init_draw_behaviour()
        self.__init_update_behaviour()
        self.__bind_mouse_events()
        self.display(image_processing_toolkit.bgr_to_rgb(self.__matrix))
        self.__push_bw_image()
        json_hints = data['hints']
        stops = np.array(data['stop'])
        counter = 0
        for hint in json_hints:
            hint_command = line_drawing_command.LineDrawingCommand.from_json(self._canvas, hint)
            hint_command.execute()
            self.__draw_behaviour.executed_commands.append(hint_command)
            self._mock_click(hint)
            counter += 1
            if counter in stops:
                self.__colorize()
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
        self.__update_behaviour.on_click(obj)
        obj.x = hint['stop'][0]
        obj.y = hint['stop'][1]
        self.__update_behaviour.on_click(obj)

    def save_state(self):
        colorization_algorithm = singleton_config.SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._state['hints'] = self.__draw_behaviour.save_state()
        return self._state

    def add_observer(self, observer):
        self.__colorized_image_subject.attach(observer)

    def add_colorization_process_observer(self, observer):
        self._colorization_process_subject.attach(observer)

    def display(self, matrix):
        self._raw_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(matrix))
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
        self._state['stop'].append(len(self.__draw_behaviour.executed_commands))
        self.__colorize()

    def __colorize(self):
        self._disable_drawing = True
        self._waiting_indicate = gui_toolkit.create_info_window("Performing colorization. Please wait...")
        bw, color = self.__get_colorization_input()
        self.__update_behaviour.perform_colorize(bw, color)
        self.after(self.__DELAY_TIME, self._check_for_cuo_result)

    def _check_for_cuo_result(self):
        result_candidate = self.__update_behaviour.check_for_result()
        if result_candidate is not None:
            x = result_candidate[0]
            y = result_candidate[1]
            result = result_candidate[2]
            result = image_processing_toolkit.bgr_matrix_to_image(result)
            result = image_processing_toolkit.bgr_to_rgb(result)

            bw, _ = self.__get_colorization_input()
            self.__colorized_image_subject.notify(x_start=x, y_start=y, result=result,
                                                  reference=bw[y:y + result.shape[0], x:x + result.shape[1]])

            self._waiting_indicate.destroy()
            self._disable_drawing = False
        else:
            self.after(self.__DELAY_TIME, self._check_for_cuo_result)

    def _check_for_ct_result(self):
        result_candidate = self._ct_async_task.result()
        if result_candidate is not None:
            result = image_processing_toolkit.bgr_to_rgb(result_candidate)
            self.__colorized_image_subject.notify(x_start=0, y_start=0, result=result, fill=True)
            self._colorization_process_subject.notify(start=True)

            self._waiting_indicate.destroy()
            self._disable_drawing = False
        else:
            self.after(self.__DELAY_TIME, self._check_for_ct_result)

    def __get_colorization_input(self):
        return self.__matrix, self.__get_scribbles_matrix()

    def __get_scribbles_matrix(self):
        scribbles_matrix = self.__matrix.copy()
        for command in self.__draw_behaviour.executed_commands:
            command.execute_on_matrix(scribbles_matrix)
        return scribbles_matrix

    def __init_canvas(self, input_matrix):
        self._image = None
        self._raw_image = None
        self._canvas = tk.Canvas(self, height=input_matrix.shape[0], width=input_matrix.shape[1], bd=0,
                                 highlightthickness=0)
        self._canvas.pack(side=tk.RIGHT)

    def __init_pencil_config(self):
        self._pencil_config_observer = pencil_config_observer.PencilConfigObserver()
        self._pencil_config = pencil_config.PencilConfig(self)
        self._pencil_config.pencil_config_subject.attach(self._pencil_config_observer)
        self._pencil_config.pack(side=tk.LEFT, padx=20)

    def __init_update_behaviour(self):
        self.__update_behaviour = update_behaviour.UpdateBehaviour(self.__matrix,
                                                                   self._pencil_config.pencil_config_subject)

    def __init_draw_behaviour(self):
        self.__draw_behaviour = draw_behaviour.DrawBehaviour(self._canvas, self._pencil_config.pencil_config_subject)

    def __bind_mouse_events(self):
        self._canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self._canvas.bind("<Button-1>", self.on_mouse_click)
        self._canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

    def __bind_mouse_events_for_load_image(self):
        self._canvas.bind("<Button-1>", self.__load_image)

    def __load_image(self, e):
        if self._disable_drawing:
            return

        colorization_algorithm = singleton_config.SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            self._image_path = image_processing_toolkit.browse_for_image('Select image to colorize')
            self._state['bw'] = self._image_path
            if self._image_path is not None:
                image = image_processing_toolkit.read_image(self._image_path)
                self.__init_bw_matrix(image)
                self.__init_pencil_config()
                self.__init_draw_behaviour()
                self.__init_update_behaviour()
                self.__bind_mouse_events()
                self.display(image_processing_toolkit.bgr_to_rgb(self.__matrix))
                self.__push_bw_image()
            else:
                self.__show_default_image()
                return
            self._colorization_process_subject.notify(start=True)
        else:
            self._image_path = image_processing_toolkit.browse_for_image('Select image to colorize')
            self._state['bw'] = self._image_path
            if self._image_path is not None:
                image = image_processing_toolkit.read_image(self._image_path)
                self.__init_bw_matrix(image)
                self.display(image_processing_toolkit.bgr_to_rgb(self.__matrix))
                self.__push_bw_image()
            else:
                self.__show_default_image()
                return

            self._image_path = image_processing_toolkit.browse_for_image('Select reference image')
            self._state['ref'] = self._image_path
            if self._image_path is not None:
                image = image_processing_toolkit.read_image(self._image_path)
                self.__init_bw_matrix(image)
                self.display(image_processing_toolkit.bgr_to_rgb(image))
                self.update()
            else:
                self.__colorized_image_subject.notify(reset=True)
                self.__show_default_image()
                return
            self.__colorize_ct(image_processing_toolkit.read_image(self._state['ref']),
                               image_processing_toolkit.read_image(self._state['bw']))

    def __colorize_ct(self, ref, bw):
        self._colorization_process_subject.notify(start=False)
        self._disable_drawing = True
        self._waiting_indicate = gui_toolkit.create_info_window("Performing colorization. Please wait...")
        self._ct_async_task.run(ref, bw)
        self.after(self.__DELAY_TIME, self._check_for_ct_result)

    def __init_bw_matrix(self, matrix):
        self.__matrix = matrix
        self.__color_matrix = matrix.copy()

    def __show_default_image(self):
        matrix = image_processing_toolkit.read_image('assets/info_load.bmp')
        if self._canvas is None:
            self.__init_canvas(matrix)
        self.__init_bw_matrix(matrix)
        self.display(matrix)

    def __init_colorized_image_subject(self):
        self.__colorized_image_subject = colorized_image_subject.ColorizedImageSubject()

    def __push_bw_image(self):
        result = image_processing_toolkit.bgr_to_rgb(self.__matrix)
        self.__colorized_image_subject.notify(x_start=0, y_start=0, result=result, fill=True)
