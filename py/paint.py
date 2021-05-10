import tkinter as tk
from tkinter import messagebox

from display_canvas import DisplayCanvas
from drawing_canvas import DrawingCanvas
from image_processing_toolkit import bgr_to_rgb, write_image
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


def init_buttons_for_image(root_node, drawing_canvas, display_canvas):
    colorize_button = tk.Button(root_node, text="Save result",
                                command=lambda: save_result(display_canvas))
    colorize_button.grid(row=1, column=2)


def save_result(display_canvas: DisplayCanvas):
    bgr_matrix = display_canvas.get_result()
    rgb_image = bgr_to_rgb(bgr_matrix)
    write_image(rgb_image, 'result.bmp')
    messagebox.showinfo("Colorization Using Optimization", "Result image saved as 'result.bmp' in working directory.")


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
    pass


def init_display_canvas_for_video(root_node):
    pass


def init_buttons_for_video(a, b, c):
    pass


if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    root.title('Colorization Using Optimization')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    init_ui(root)

    root.mainloop()
