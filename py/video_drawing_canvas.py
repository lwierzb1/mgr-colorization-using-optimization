import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from draw_behaviour import DrawBehaviour
from gui_toolkit import create_info_window
from image_processing_toolkit import bgr_to_rgb, read_image, bgr_matrix_to_image, browse_for_video
from pencil_config import PencilConfig
from pencil_config_observer import PencilConfigObserver
from colorized_image_subject import ColorizedImageSubject
from image_colorizer_multiprocess import ImageColorizerMultiprocess
from py.colorization_process_subject import ColorizationProcessSubject
from singleton_config import SingletonConfig
from video_optimization_colorizer import VideoOptimizationColorizer
from video_transfer_colorizer import VideoTransferColorizer
from update_behaviour import UpdateBehaviour


class VideoDrawingCanvas(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self._raw_image = None
        self._image = None
        self._video_colorizer = None
        self._colorization_process_subject = ColorizationProcessSubject()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.__show_default_image()
        self.__bind_mouse_events_for_load_image()
        self.__init_colorized_image_subject()
        self._colorization_process_subject.notify(start=False)

    def force_save_video(self):
        self._video_colorizer.force_save()

    def add_observer(self, observer):
        self.__colorized_image_subject.attach(observer)

    def add_colorization_process_observer(self, observer):
        self._colorization_process_subject.attach(observer)

    def go_next(self):
        window = create_info_window("Performing colorization. Please wait...")
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            color = self.__get_scribbles_matrix()
            self._video_colorizer.colorize_video(color)
            first_frame = self._video_colorizer.get_frame_to_colorize()

            self.__init_bw_matrix(first_frame)
            self.display(bgr_to_rgb(self.__matrix))
            self.__push_bw_image()
        else:
            bw, color = self.__get_colorization_input()
            colorizer = ImageColorizerMultiprocess(bw, color)
            result = colorizer.colorize()
            result = bgr_matrix_to_image(result)
            self._video_colorizer.colorize_video(result)

        window.destroy()

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
        self.__draw_behaviour.draw(e)
        self.__update_behaviour.on_motion(e)

    def on_mouse_click(self, e):
        self.__draw_behaviour.draw_dot(e)
        self.__update_behaviour.on_click(e)

    def on_mouse_release(self, e):
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

    def __bind_mouse_events_for_load_image(self):
        self._canvas.bind("<Button-1>", self.__load_image)

    def __load_image(self, e):
        video_filename = browse_for_video()
        if video_filename is not None:
            colorization_algorithm = SingletonConfig().colorization_algorithm

            if colorization_algorithm == 'CUO':
                self._video_colorizer = VideoOptimizationColorizer(self.__colorized_image_subject, video_filename)
                first_frame = self._video_colorizer.get_frame_to_colorize()
            else:
                self._video_colorizer = VideoTransferColorizer(self.__colorized_image_subject, video_filename)
                first_frame = self._video_colorizer.get_first_frame()

            self.__init_bw_matrix(first_frame)
            self.__init_pencil_config()
            self.__init_draw_behaviour()
            self.__init_update_behaviour()
            self.__bind_mouse_events()
            self.display(bgr_to_rgb(self.__matrix))
            self.__push_bw_image()
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
