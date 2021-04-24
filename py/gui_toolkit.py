import tkinter as tk


def create_info_window(text):
    window = tk.Toplevel()
    window.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    window.geometry("+%d+%d" % (x, y))

    label = tk.Label(window, text=text)
    label.pack()
    window.lift()
    window.update()
    return window
