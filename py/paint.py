import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

from display_canvas import DisplayCanvas
from drawing_canvas import DrawingCanvas
from image_processing_toolkit import bgr_to_rgb, write_image
from video_display_canvas import VideoDisplayCanvas
from video_drawing_canvas import VideoDrawingCanvas
from singleton_config import SingletonConfig


def init_ui(root_node):
    mode = SingletonConfig.get_instance().mode
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
    menu = tk.Menu(root_node)
    menu.add_cascade(label='SAVE RESULT', command=lambda: save_result(display_canvas))
    menu.add_separator()
    menu.add_cascade(label='RESET', command=lambda: reset_ui_image(root_node, drawing_canvas, display_canvas))
    menu.add_separator()
    menu.add_cascade(label='ABOUT', command=lambda: show_about())
    root_node.config(menu=menu)


def save_result(display_canvas: DisplayCanvas):
    bgr_matrix = display_canvas.get_result()
    rgb_image = bgr_to_rgb(bgr_matrix)
    write_image(rgb_image, 'result.bmp')
    messagebox.showinfo("Colorization Using Optimization",
                        "Result image saved as " + get_working_directory() + "/result.bmp.")


def save_result_video(drawing_canvas: VideoDrawingCanvas):
    drawing_canvas.force_save_video()
    messagebox.showinfo("Colorization Using Optimization",
                        "Result video saved as " + get_working_directory() + "/result.avi.")


def show_about():
    messagebox.showinfo("Colorization Using Optimization",
                        "Master Thesis Colorization Program.\nAuthor: Łukasz Wierzbicki, 277446.")


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
    colorization_algorithm = SingletonConfig.get_instance().colorization_algorithm
    if colorization_algorithm == 'CUO':
        display = VideoDisplayCanvas(root_node)
    else:
        display = DisplayCanvas(root_node)
    display.grid(row=0, column=1)
    return display


def init_buttons_for_video(root_node, drawing_canvas, display_canvas):
    menu = tk.Menu(root_node)
    menu.add_cascade(label='PERFORM COLORIZE', command=lambda: drawing_canvas.go_next())
    menu.add_separator()
    menu.add_cascade(label='SAVE RESULT', command=lambda: save_result_video(drawing_canvas))
    menu.add_separator()
    menu.add_cascade(label='RESET', command=lambda: reset_ui_video(root_node, drawing_canvas, display_canvas))
    menu.add_separator()
    menu.add_cascade(label='ABOUT', command=lambda: show_about())
    root_node.config(menu=menu)


def get_working_directory():
    return os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style(root)
    root.tk.call('source', 'style/azure.tcl')
    style.theme_use('azure')

    root.state('zoomed')
    root.title('Colorization Using Optimization')
    root.style = ttk.Style(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    init_ui(root)

    root.mainloop()
