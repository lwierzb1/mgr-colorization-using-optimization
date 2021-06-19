import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfile

import src.config.singleton_config
import src.gui.config_picker
import src.gui.video_display_canvas
import src.gui.video_drawing_canvas
import src.toolkit.gui
import src.toolkit.image_processing
from src.config.singleton_config import SingletonConfig
from src.gui.display_canvas import DisplayCanvas
from src.gui.drawing_canvas import DrawingCanvas
from src.gui.styled_observer_button import StyledObserverButton
from src.gui.video_display_canvas import VideoDisplayCanvas
from src.gui.video_drawing_canvas import VideoDrawingCanvas
from src.toolkit.gui import create_info_confirm_window
from src.toolkit.image_processing import write_image, bgr_to_rgb


class MainWindow:
    def __init__(self):
        self._root = tk.Tk()
        self._prepare_style()
        self._init_buttons_for_pick_config()

    def main_loop(self):
        self._root.mainloop()

    def _init_buttons_for_pick_config(self):
        buttons_frame = ttk.Frame(self._root)
        restore_state_button = StyledObserverButton(buttons_frame, text='RESTORE STATE', style='AccentButton',
                                                    command=self._restore_state)
        config_button = StyledObserverButton(buttons_frame, text='PICK CONFIG', style='AccentButton',
                                             command=self._pick_config)
        about_button = StyledObserverButton(buttons_frame, text='ABOUT', style='AccentButton',
                                            command=self._show_about)

        restore_state_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        config_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        about_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        buttons_frame.grid(row=0, column=0, columnspan=3, rowspan=2)

    def _prepare_style(self):
        style = ttk.Style(self._root)
        self._root.tk.call('source', '../style/azure.tcl')
        style.theme_use('azure')

        self._root.iconphoto(True, tk.PhotoImage(file='../assets/icon.png'))

        self._root.title('Colorization Program')
        self._root.style = ttk.Style(self._root)

        self._root.style.configure("AccentButton", font=('calibri', 18))
        self._root.style.configure("BW.TLabel", foreground="#000000", background="#ffffff")
        self._root.style.configure('TEntry', foreground='#000000')
        self._root.style.configure('TCombobox', foreground='#000000')

        self._root.option_add("*TCombobox*background", "#ffffff")
        self._root.option_add("*TCombobox*foreground", "#000000")
        self._root.option_add("*TCombobox*font", "calibri 18")
        self._root.option_add("*TCombobox*selectBackground", "#bebebe")
        self._root.option_add("*TCombobox*selectBackground", "#bebebe")

        self._root.option_add("*TLabel*font", "calibri 18")

        self._root.option_add("*TEntry*font", "calibri 18")
        self._root.option_add("*TEntry*background", "#ffffff")
        self._root.option_add("*TEntry*foreground", "#000000")

        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_columnconfigure(1, weight=1)
        self._root.grid_rowconfigure(0, weight=1)

        self._root.grid_columnconfigure(0, weight=40)
        self._root.grid_columnconfigure(1, weight=40)
        self._root.grid_columnconfigure(2, weight=20)
        w, h = self._root.winfo_screenwidth(), self._root.winfo_screenheight()
        self._root.geometry("%dx%d+0+0" % (w, h))

    def _init_ui(self):
        for widget in self._root.winfo_children():
            widget.destroy()
        mode = SingletonConfig().mode
        if mode == 'image':
            drawing = self._init_drawing_canvas_for_image()
            display = self._init_display_canvas_for_image()
            drawing.add_observer(display)
            self._init_buttons_for_image(drawing, display)
        else:
            drawing = self._init_drawing_canvas_for_video()
            display = self._init_display_canvas_for_video()
            drawing.add_observer(display)
            self._init_buttons_for_video(drawing, display)
        return drawing, display

    def _reset_ui_image(self, drawing_canvas, display_canvas):
        drawing_canvas.destroy()
        display_canvas.destroy()
        drawing = self._init_drawing_canvas_for_image()
        display = self._init_display_canvas_for_image()
        drawing.add_observer(display)
        self._init_buttons_for_image(drawing, display)

    def _reset_ui_video(self, drawing_canvas, display_canvas):
        drawing_canvas.destroy()
        display_canvas.destroy()
        drawing = self._init_drawing_canvas_for_video()
        display = self._init_display_canvas_for_video()
        drawing.add_observer(display)
        self._init_buttons_for_video(drawing, display)

    def _init_buttons_for_image(self, drawing_canvas, display_canvas):
        buttons_frame = ttk.Frame(self._root)
        save_result_button = StyledObserverButton(buttons_frame, text='SAVE RESULT',
                                                  style='AccentButton',
                                                  command=lambda: self._save_result(display_canvas),
                                                  state=tk.DISABLED)
        reset_button = StyledObserverButton(buttons_frame, text='RESET', style='AccentButton',
                                            command=lambda: self._reset_ui_image(drawing_canvas,
                                                                                 display_canvas),
                                            state=tk.DISABLED)
        save_state_button = StyledObserverButton(buttons_frame, text='SAVE STATE',
                                                 style='AccentButton',
                                                 command=lambda: self._save_state(drawing_canvas),
                                                 state=tk.DISABLED)
        restore_state_button = StyledObserverButton(buttons_frame, text='RESTORE STATE',
                                                    style='AccentButton',
                                                    command=self._restore_state)
        config_button = StyledObserverButton(buttons_frame, text='PICK CONFIG',
                                             style='AccentButton',
                                             command=self._pick_config)
        about_button = StyledObserverButton(buttons_frame, text='ABOUT', style='AccentButton',
                                            command=self._show_about)

        save_result_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        reset_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        save_state_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        restore_state_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        config_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        about_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)

        drawing_canvas.add_colorization_process_observer(save_result_button)
        drawing_canvas.add_colorization_process_observer(reset_button)
        drawing_canvas.add_colorization_process_observer(save_state_button)
        drawing_canvas.add_colorization_process_observer(restore_state_button)
        drawing_canvas.add_colorization_process_observer(config_button)

        buttons_frame.grid(row=0, column=2)

    def _pick_config(self):
        window = tk.Toplevel(self._root)
        src.gui.config_picker.ConfigPicker(window, self._callback)
        window.attributes('-topmost', 'true')
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - size[0] / 2
        y = screen_height / 2 - size[1] / 2

        window.geometry("+%d+%d" % (x, y))

    def _save_result(self, display_canvas: DisplayCanvas):
        bgr_matrix = display_canvas.image_array
        rgb_image = bgr_to_rgb(bgr_matrix)
        write_image(rgb_image, 'result.bmp')
        create_info_confirm_window("Result image saved as " + self._get_working_directory() + "/result.bmp.")

    def _save_result_video(self, drawing_canvas: VideoDrawingCanvas):
        drawing_canvas.force_save_video()
        create_info_confirm_window("Result video saved as " + self._get_working_directory() + "/result.avi.")

    @staticmethod
    def _show_about():
        create_info_confirm_window('Master Thesis Colorization Program.\nAuthor: Łukasz Wierzbicki, 277446.')

    @staticmethod
    def _save_state(drawing):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".json",
                                        filetypes=(("JSON file", "*.json"), ("All Files", "*.*")))

        if file:
            drawing_canvas_state = drawing.save_state()
            config_state = SingletonConfig().save_state()
            state_value = json.dumps(drawing_canvas_state | config_state)
            file.write(state_value)

            file.close()

    def _restore_state(self):
        file = askopenfile(mode='r', filetypes=[('JSON files', '*.json')])
        if file is not None:
            data = json.load(file)
            SingletonConfig().restore_state(data)
            drawing, _ = self._init_ui()

            drawing.restore_state(data)

    def _init_drawing_canvas_for_image(self):
        drawing = DrawingCanvas(self._root)
        drawing.grid(row=0, column=0)
        self._root.bind('<Control-z>', drawing.undo_last_command)
        self._root.bind('<Control-y>', drawing.redo_last_command)
        return drawing

    def _init_display_canvas_for_image(self):
        display = DisplayCanvas(self._root)
        display.grid(row=0, column=1)
        return display

    def _init_drawing_canvas_for_video(self):
        drawing = VideoDrawingCanvas(self._root)
        drawing.grid(row=0, column=0)
        self._root.bind('<Control-z>', drawing.undo_last_command)
        self._root.bind('<Control-y>', drawing.redo_last_command)
        return drawing

    def _init_display_canvas_for_video(self):
        colorization_algorithm = SingletonConfig().colorization_algorithm
        if colorization_algorithm == 'CUO':
            display = VideoDisplayCanvas(self._root)
        else:
            display = DisplayCanvas(self._root)
        display.grid(row=0, column=1)
        return display

    def _init_buttons_for_video(self, drawing_canvas, display_canvas):
        buttons_frame = ttk.Frame(self._root)
        colorize_button = StyledObserverButton(buttons_frame, text='PERFORM COLORIZE', style='AccentButton',
                                               command=drawing_canvas.go_next, state=tk.DISABLED)
        save_result_button = StyledObserverButton(buttons_frame, text='SAVE RESULT', style='AccentButton',
                                                  command=lambda: self._save_result_video(drawing_canvas),
                                                  state=tk.DISABLED)
        reset_button = StyledObserverButton(buttons_frame, text='RESET', style='AccentButton',
                                            command=lambda: self._reset_ui_video(drawing_canvas, display_canvas),
                                            state=tk.DISABLED)
        save_state_button = StyledObserverButton(buttons_frame, text='SAVE STATE', style='AccentButton',
                                                 command=lambda: self._save_state(drawing_canvas))
        restore_state_button = StyledObserverButton(buttons_frame, text='RESTORE STATE', style='AccentButton',
                                                    command=self._restore_state)
        config_button = StyledObserverButton(buttons_frame, text='PICK CONFIG', style='AccentButton',
                                             command=self._pick_config)
        about_button = StyledObserverButton(buttons_frame, text='ABOUT', style='AccentButton',
                                            command=self._show_about)

        colorize_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        save_result_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        reset_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        save_state_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        restore_state_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        config_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)
        about_button.pack(fill=tk.BOTH, pady=10, ipady=10, ipadx=10)

        drawing_canvas.add_colorization_process_observer(colorize_button)
        drawing_canvas.add_colorization_process_observer(save_result_button)
        drawing_canvas.add_colorization_process_observer(reset_button)
        drawing_canvas.add_colorization_process_observer(save_state_button)
        drawing_canvas.add_colorization_process_observer(config_button)
        drawing_canvas.add_colorization_process_observer(restore_state_button)

        buttons_frame.grid(row=0, column=2)

    @staticmethod
    def _get_working_directory():
        return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

    def _callback(self, conf):
        SingletonConfig().mode = conf['mode']
        SingletonConfig().colorization_algorithm = conf['colorization_algorithm']
        SingletonConfig().linear_algorithm = conf['linear_algorithm']
        SingletonConfig().processes = conf['processes']
        SingletonConfig().max_video_frames_per_section = conf['max_video_frames_per_section']
        SingletonConfig().jacobi_approximation = conf['jacobi_approximation']
        SingletonConfig().k_means = conf['k_means']
        SingletonConfig().edge_detection = conf['edge_detection']
        self._init_ui()
