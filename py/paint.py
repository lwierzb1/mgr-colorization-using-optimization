import tkinter as tk

from display_canvas import DisplayCanvas
from py.drawing_canvas import DrawingCanvas
from image_colorizer_multiprocess import ImageColorizerMultiprocess
from image_processing_toolkit import bgr_matrix_to_image, bgr_to_rgb
import cv2
from update_grid import UpdateGrid


def init_ui(root_node):
    drawing = init_drawing_canvas(root_node)
    display = init_display_canvas(root_node)
    init_buttons(root_node, drawing, display)


def init_buttons(root_node, drawing_canvas, display_canvas):
    colorize_button = tk.Button(root_node, text="Colorize",
                                command=lambda: perform_colorize(drawing_canvas, display_canvas))
    colorize_button.grid(row=1, column=2)


def init_drawing_canvas(root_node):
    drawing = DrawingCanvas(root_node)
    drawing.grid(row=0, column=0)
    root_node.bind('<Control-z>', drawing.undo_last_command)
    root_node.bind('<Control-y>', drawing.redo_last_command)
    return drawing


def init_display_canvas(root_node):
    display = DisplayCanvas(root_node)
    display.grid(row=0, column=1)
    return display


def perform_colorize(drawing: DrawingCanvas, display: DisplayCanvas):
    bw, scribbles = drawing.get_colorization_input()
    colorizer = ImageColorizerMultiprocess(bw, scribbles)
    colorized_matrix = colorizer.colorize()
    colorized_bgr_image = bgr_matrix_to_image(colorized_matrix)
    colorized_rgb_image = bgr_to_rgb(colorized_bgr_image)
    display.display(colorized_rgb_image)


if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # y = cv2.resize(y, (100, 100))
    init_ui(root)

    root.mainloop()
