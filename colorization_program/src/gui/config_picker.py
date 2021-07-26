__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import multiprocessing
import tkinter as tk
from tkinter import ttk


class ConfigPicker(ttk.Frame):
    def __init__(self, master, callback, **kw):
        super().__init__(master, **kw)
        self._callback = callback
        self._only_integers = (
            self.register(self._only_integers_callback), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self._only_floats = (
            self.register(self._only_floats_callback), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self._init_mode()
        self._init_colorization_algorithm()
        self._init_linear_algorithm()
        self._init_process_number()
        self._init_jacobi_approximation()
        self._init_max_frames_per_section()
        self._apply_k_mean()
        self._apply_edge_detection()
        self._init_accept_button()
        self.grid(padx=20, pady=20)
        self.pack()

    def _init_mode(self):
        self._mode = tk.StringVar()
        ttk.Label(self, text="Select mode", style="BW.TLabel").grid(column=0,
                                                                    row=0, padx=10, pady=25, sticky='w')

        mode_chooser = ttk.Combobox(self, textvariable=self._mode, state="readonly")

        mode_chooser['values'] = ('Image',
                                  'Video')

        mode_chooser.grid(column=1, row=0, sticky='e', padx=(0, 10))

        mode_chooser.current(0)

    def _init_linear_algorithm(self):
        self._linear_algorithm = tk.StringVar()
        ttk.Label(self, text="Select linear algorithm", style="BW.TLabel").grid(column=0,
                                                                                row=2, padx=10, pady=25, sticky='w')

        linear_algorithm_chooser = ttk.Combobox(self, state="readonly", textvariable=self._linear_algorithm)

        linear_algorithm_chooser['values'] = ('Jacobi',
                                              'Spsolve',
                                              'LGMRES')

        linear_algorithm_chooser.grid(column=1, row=2, sticky='e', padx=(0, 10))

        linear_algorithm_chooser.current(2)

    def _init_colorization_algorithm(self):
        self._colorization_algorithm = tk.StringVar()
        ttk.Label(self, text="Select colorization algorithm", style="BW.TLabel").grid(column=0,
                                                                                      row=1, padx=10, pady=25,
                                                                                      sticky='w')

        colorization_algorithm_chooser = ttk.Combobox(self, width=35, state="readonly",
                                                      textvariable=self._colorization_algorithm)

        colorization_algorithm_chooser['values'] = ('Colorization Using Optimization',
                                                    'Transferring Color to Greyscale Image')

        colorization_algorithm_chooser.grid(column=1, row=1, sticky='e', padx=(0, 10))

        colorization_algorithm_chooser.current(0)

    def _init_process_number(self):
        label_content = "Select number of processes (max = {})".format(multiprocessing.cpu_count())
        ttk.Label(self, text=label_content, style="BW.TLabel").grid(column=0,
                                                                    row=3, padx=10, pady=25, sticky='w')

        self._process_number = tk.StringVar(self, multiprocessing.cpu_count())
        entry = ttk.Entry(self, validate="key", validatecommand=self._only_integers, textvariable=self._process_number)
        entry.grid(column=1, row=3, sticky='e', padx=(0, 10))

    def _init_jacobi_approximation(self):
        ttk.Label(self, text="Specify Jacobi approximation (If needed)", style="BW.TLabel").grid(column=0,
                                                                                                 row=4, padx=10,
                                                                                                 pady=25, sticky='w')
        self._jacobi_approximation = tk.StringVar(self, '0.001')
        jacobi_approximation_input = ttk.Entry(self, validate='key', validatecommand=self._only_floats,
                                               textvariable=self._jacobi_approximation)

        jacobi_approximation_input.grid(column=1, row=4, sticky='e', padx=(0, 10))

    def _init_max_frames_per_section(self):
        ttk.Label(self, text="Specify max video frames per section (If needed)", style="BW.TLabel").grid(column=0,
                                                                                                         row=5, padx=10,
                                                                                                         pady=25,
                                                                                                         sticky='w')
        self._max_frames_per_section = tk.StringVar(self, '10')
        max_frames_per_section_input = ttk.Entry(self, validate='key', validatecommand=self._only_integers,
                                                 textvariable=self._max_frames_per_section)

        max_frames_per_section_input.grid(column=1, row=5, sticky='e', padx=(0, 10))

    def _apply_k_mean(self):
        ttk.Label(self, text="K-means with Transferring Color to Greyscale Image", style="BW.TLabel").grid(column=0,
                                                                                                           row=6,
                                                                                                           padx=10,
                                                                                                           pady=25,
                                                                                                           sticky='w')
        self._should_apply_k_mean = tk.BooleanVar(self, True)
        check_button = ttk.Checkbutton(self, text='', style='Switch', variable=self._should_apply_k_mean)
        check_button.grid(column=1, row=6, sticky='e', padx=(0, 10))

    def _apply_edge_detection(self):
        ttk.Label(self, text="Edge detection with Colorization Using Optimization", style="BW.TLabel").grid(column=0,
                                                                                                            row=7,
                                                                                                            padx=10,
                                                                                                            pady=25,
                                                                                                            sticky='w')
        self._should_apply_edge_detection = tk.BooleanVar(self, True)
        check_button = ttk.Checkbutton(self, text='', style='Switch', variable=self._should_apply_edge_detection)
        check_button.grid(column=1, row=7, sticky='e', padx=(0, 10))

    def _init_accept_button(self):
        button = ttk.Button(self, text='ACCEPT', width=40, style='AccentButton', command=self._save_config)
        button.grid(row=8, column=0, columnspan=2, pady=10)

    def _save_config(self):
        config = dict()
        config['mode'] = self._mode.get().lower()
        config['jacobi_approximation'] = float(self._jacobi_approximation.get())
        config['processes'] = int(self._process_number.get())
        config['max_video_frames_per_section'] = int(self._max_frames_per_section.get())
        config['linear_algorithm'] = self._linear_algorithm.get().lower()
        config['k_means'] = self._should_apply_k_mean.get()
        config['edge_detection'] = self._should_apply_edge_detection.get()

        if "optimization" in self._colorization_algorithm.get().lower():
            config['colorization_algorithm'] = 'CUO'
        else:
            config['colorization_algorithm'] = 'CT'

        self._callback(config)
        self.master.destroy()

    def _only_integers_callback(self, d, i, P, s, S, v, V, W):
        return str.isdecimal(P) or P == ''

    def _only_floats_callback(self, d, i, P, s, S, v, V, W):
        try:
            float(P)
            return True
        except ValueError:
            return False
