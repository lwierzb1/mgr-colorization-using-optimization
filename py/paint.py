import json
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import os
from tkinter.filedialog import askopenfile

from display_canvas import DisplayCanvas
from drawing_canvas import DrawingCanvas
from image_processing_toolkit import bgr_to_rgb, write_image
from config_picker import ConfigPicker
from styled_observer_button import StyledObserverButton
from video_display_canvas import VideoDisplayCanvas
from video_drawing_canvas import VideoDrawingCanvas
from singleton_config import SingletonConfig


def init_ui(root_node):
    for widget in root_node.winfo_children():
        widget.destroy()
    mode = SingletonConfig().mode
    if mode == 'image':
        drawing = init_drawing_canvas_for_image(root_node)
        display = init_display_canvas_for_image(root_node)
        drawing.add_observer(display)
        init_buttons_for_image(root_node, drawing, display)
    else:
        drawing = init_drawing_canvas_for_video(root_node)
        display = init_display_canvas_for_video(root_node)
        drawing.add_observer(display)
        init_buttons_for_video(root_node, drawing, display)


def reset_ui_image(root_node, drawing_canvas, display_canvas):
    drawing_canvas.destroy()
    display_canvas.destroy()
    drawing = init_drawing_canvas_for_image(root_node)
    display = init_display_canvas_for_image(root_node)
    drawing.add_observer(display)
    init_buttons_for_image(root_node, drawing, display)


def reset_ui_video(root_node, drawing_canvas, display_canvas):
    drawing_canvas.destroy()
    display_canvas.destroy()
    drawing = init_drawing_canvas_for_video(root_node)
    display = init_display_canvas_for_video(root_node)
    drawing.add_observer(display)
    init_buttons_for_video(root_node, drawing, display)


def init_buttons_for_image(root_node, drawing_canvas, display_canvas):
    buttons_frame = ttk.Frame(root_node)
    save_result_button = StyledObserverButton(buttons_frame, text='SAVE RESULT', style='AccentButton',
                                              command=lambda: save_result(display_canvas), state=tk.DISABLED)
    reset_button = StyledObserverButton(buttons_frame, text='RESET', style='AccentButton',
                                        command=lambda: reset_ui_image(root_node, drawing_canvas, display_canvas),
                                        state=tk.DISABLED)
    save_state_button = StyledObserverButton(buttons_frame, text='SAVE STATE', style='AccentButton',
                                             command=lambda: save_state(drawing_canvas), state=tk.DISABLED)
    restore_state_button = StyledObserverButton(buttons_frame, text='RESTORE STATE', style='AccentButton',
                                                command=lambda: restore_state(drawing_canvas, display_canvas))
    config_button = StyledObserverButton(buttons_frame, text='PICK CONFIG', style='AccentButton',
                                         command=lambda: pick_config())
    about_button = StyledObserverButton(buttons_frame, text='ABOUT', style='AccentButton',
                                        command=lambda: show_about())

    save_result_button.pack(fill=tk.BOTH, pady=10)
    reset_button.pack(fill=tk.BOTH, pady=10)
    save_state_button.pack(fill=tk.BOTH, pady=10)
    restore_state_button.pack(fill=tk.BOTH, pady=10)
    config_button.pack(fill=tk.BOTH, pady=10)
    about_button.pack(fill=tk.BOTH, pady=10)

    drawing_canvas.add_colorization_process_observer(save_result_button)
    drawing_canvas.add_colorization_process_observer(reset_button)
    drawing_canvas.add_colorization_process_observer(save_state_button)
    drawing_canvas.add_colorization_process_observer(save_result_button)

    buttons_frame.grid(row=0, column=2)


def pick_config():
    window = tk.Toplevel()
    ConfigPicker(window, callback)


def save_result(display_canvas: DisplayCanvas):
    bgr_matrix = display_canvas.get_result()
    rgb_image = bgr_to_rgb(bgr_matrix)
    write_image(rgb_image, 'result.bmp')
    messagebox.showinfo("Colorization Program",
                        "Result image saved as " + get_working_directory() + "/result.bmp.")


def save_result_video(drawing_canvas: VideoDrawingCanvas):
    drawing_canvas.force_save_video()
    messagebox.showinfo("Colorization Program",
                        "Result video saved as " + get_working_directory() + "/result.avi.")


def show_about():
    messagebox.showinfo("Colorization Program",
                        "Master Thesis Colorization Program.\nAuthor: Łukasz Wierzbicki, 277446.")


def save_state(drawing):
    file = filedialog.asksaveasfile(mode='w', defaultextension=".json",
                                    filetypes=(("JSON file", "*.json"), ("All Files", "*.*")))

    if file:
        drawing_canvas_state = drawing.save_state()
        config_state = SingletonConfig().save_state()
        state_value = json.dumps(drawing_canvas_state | config_state)
        file.write(state_value)

        file.close()


def restore_state(drawing, display):
    file = askopenfile(mode='r', filetypes=[('JSON files', '*.json')])
    if file is not None:
        data = json.load(file)
        SingletonConfig().restore_state(data)
        drawing.restore_state(data)


def init_drawing_canvas_for_image(root_node):
    drawing = DrawingCanvas(root_node)
    drawing.grid(row=0, column=0)
    root_node.bind('<Control-z>', drawing.undo_last_command)
    root_node.bind('<Control-y>', drawing.redo_last_command)
    return drawing


def init_display_canvas_for_image(root_node):
    display = DisplayCanvas(root_node)
    display.grid(row=0, column=1)
    return display


def init_drawing_canvas_for_video(root_node):
    drawing = VideoDrawingCanvas(root_node)
    drawing.grid(row=0, column=0)
    root_node.bind('<Control-z>', drawing.undo_last_command)
    root_node.bind('<Control-y>', drawing.redo_last_command)
    return drawing


def init_display_canvas_for_video(root_node):
    colorization_algorithm = SingletonConfig().colorization_algorithm
    if colorization_algorithm == 'CUO':
        display = VideoDisplayCanvas(root_node)
    else:
        display = DisplayCanvas(root_node)
    display.grid(row=0, column=1)
    return display


def init_buttons_for_video(root_node, drawing_canvas, display_canvas):
    buttons_frame = ttk.Frame(root_node)
    save_result_button = StyledObserverButton(buttons_frame, text='PERFORM COLORIZE', style='AccentButton',
                                              command=lambda: drawing_canvas.go_next(), state=tk.DISABLED)
    reset_button = StyledObserverButton(buttons_frame, text='SAVE RESULT', style='AccentButton',
                                        command=lambda: save_result_video(drawing_canvas),
                                        state=tk.DISABLED)
    save_state_button = StyledObserverButton(buttons_frame, text='RESET', style='AccentButton',
                                             command=lambda: reset_ui_video(root_node, drawing_canvas, display_canvas),
                                             state=tk.DISABLED)
    restore_state_button = StyledObserverButton(buttons_frame, text='RESTORE STATE', style='AccentButton',
                                                command=lambda: restore_state(drawing_canvas, display_canvas))
    config_button = StyledObserverButton(buttons_frame, text='PICK CONFIG', style='AccentButton',
                                         command=lambda: pick_config())
    about_button = StyledObserverButton(buttons_frame, text='ABOUT', style='AccentButton',
                                        command=lambda: show_about())

    save_result_button.pack(fill=tk.BOTH, pady=10)
    reset_button.pack(fill=tk.BOTH, pady=10)
    save_state_button.pack(fill=tk.BOTH, pady=10)
    restore_state_button.pack(fill=tk.BOTH, pady=10)
    config_button.pack(fill=tk.BOTH, pady=10)
    about_button.pack(fill=tk.BOTH, pady=10)

    drawing_canvas.add_colorization_process_observer(save_result_button)
    drawing_canvas.add_colorization_process_observer(reset_button)
    drawing_canvas.add_colorization_process_observer(save_state_button)
    drawing_canvas.add_colorization_process_observer(save_result_button)

    buttons_frame.grid(row=0, column=2)


def get_working_directory():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


def callback(conf):
    SingletonConfig().mode = conf['mode']
    SingletonConfig().colorization_algorithm = conf['colorization_algorithm']
    SingletonConfig().linear_algorithm = conf['linear_algorithm']
    SingletonConfig().processes = conf['processes']
    SingletonConfig().max_video_frames_per_section = conf['max_video_frames_per_section']
    SingletonConfig().jacobi_approximation = conf['jacobi_approximation']
    init_ui(root)
    root.state('zoomed')


if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    root.tk.call('source', 'style/azure.tcl')
    style.theme_use('azure')

    root.title('Colorization Program')
    root.style = ttk.Style(root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.grid_columnconfigure(0, weight=40)
    root.grid_columnconfigure(1, weight=40)
    root.grid_columnconfigure(2, weight=20)
    root.wm_state('iconic')

    pick_config()
    root.mainloop()
