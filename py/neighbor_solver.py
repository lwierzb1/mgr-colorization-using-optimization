#!/usr/bin/env python
"""
This file is part of Colorization Using Optimization implementation in Python.
Class that searches the surroundings of a given point in order to find neighbors.
"""

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


class NeighborSolver:
    def __init__(self, center, y_channel):
        self.__window_width = 1
        self.__center = [center[0], center[1], y_channel]
        self.__y_channel = y_channel

    def find_neighbors(self, weights):
        neighbors = []
        image_rows = self.__y_channel.shape[0]
        image_cols = self.__y_channel.shape[1]
        window_r_min = max(0, self.__center[0] - self.__window_width)
        window_r_max = min(image_rows, self.__center[0] + self.__window_width + 1)
        window_c_min = max(0, self.__center[1] - self.__window_width)
        window_c_max = min(image_cols, self.__center[1] + self.__window_width + 1)
        for r in range(window_r_min, window_r_max):
            for c in range(window_c_min, window_c_max):
                row = self.__center[0] * image_cols + self.__center[1]
                col = r * image_cols + c
                if r == self.__center[0] and c == self.__center[1]:
                    weights.append((row, col, 1.))
                else:
                    neighbors.append((row, col, self.__y_channel[r, c]))
        return neighbors
