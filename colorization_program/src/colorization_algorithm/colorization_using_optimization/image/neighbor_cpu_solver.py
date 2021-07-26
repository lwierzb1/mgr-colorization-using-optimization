__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import numpy as np

import neighbor_solver


class NeighborCpuSolver(neighbor_solver.NeighborSolver):
    def __init__(self):
        super().__init__()
        self._WINDOW_WIDTH = 3

    def find_neighbors(self, center, y_channel):
        neighbors = []
        image_rows = y_channel.shape[0]
        image_cols = y_channel.shape[1]
        window_r_min = max(0, center[0] - self._WINDOW_WIDTH)
        window_r_max = min(image_rows, center[0] + self._WINDOW_WIDTH + 1)
        window_c_min = max(0, center[1] - self._WINDOW_WIDTH)
        window_c_max = min(image_cols, center[1] + self._WINDOW_WIDTH + 1)
        for r in range(window_r_min, window_r_max):
            for c in range(window_c_min, window_c_max):
                if r == center[0] and c == center[1]:
                    continue
                else:
                    neighbors.append((r, c, y_channel[r, c]))
        return np.array(neighbors)
