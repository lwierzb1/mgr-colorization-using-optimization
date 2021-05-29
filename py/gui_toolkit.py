import tkinter as tk
from tkinter import ttk


def create_info_window(text):
    window = tk.Toplevel()
    window.update_idletasks()
    window.attributes('-disabled', True)

    # Tkinter way to find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    window.geometry("+%d+%d" % (x, y))

    label = ttk.Label(window, text=text, style="BW.TLabel")
    label.pack(padx=10, pady=10)

    progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, mode='indeterminate', length=200)
    progress_bar.start()
    progress_bar.pack()

    window.lift()
    window.update()
    return window


def create_info_confirm_window(text):
    window = tk.Toplevel()
    window.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    window.geometry("+%d+%d" % (x, y))

    label = ttk.Label(window, text=text, style="BW.TLabel")
    label.pack(padx=10, pady=10)

    button = ttk.Button(window, style='AccentButton', text="OK", command=lambda: window.destroy())
    button.pack(fill=tk.BOTH, pady=10, padx=10)

    window.lift()
    window.update()
    return window
