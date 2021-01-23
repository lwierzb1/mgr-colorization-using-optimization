#!/usr/bin/env python
__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


class NeighborSolver:
    """
       A class used to solve finding Y channel value of neighbor for given pixel.

       Attributes
       ----------
       __center
           pixel around which we are looking for neighbors

      __WINDOW_WIDTH
           the width of the search window

       Methods
       -------
       find_neighbors(weights)
           Finds neighbors for given pixel.
           If the analyzed pixel is the pixel around which we are looking for neighbors, the weight should be increased
       """

    def __init__(self, center, y_channel):
        self.__WINDOW_WIDTH = 3
        self.__center = [center[0], center[1], y_channel]
        self.__y_channel = y_channel

    def find_neighbors(self, weights):
        neighbors = []
        image_rows = self.__y_channel.shape[0]
        image_cols = self.__y_channel.shape[1]
        window_r_min = max(0, self.__center[0] - self.__WINDOW_WIDTH)
        window_r_max = min(image_rows, self.__center[0] + self.__WINDOW_WIDTH + 1)
        window_c_min = max(0, self.__center[1] - self.__WINDOW_WIDTH)
        window_c_max = min(image_cols, self.__center[1] + self.__WINDOW_WIDTH + 1)
        for r in range(window_r_min, window_r_max):
            for c in range(window_c_min, window_c_max):
                row = self.__center[0] * image_cols + self.__center[1]
                col = r * image_cols + c
                if r == self.__center[0] and c == self.__center[1]:
                    weights.append((row, col, 1.))
                else:
                    neighbors.append((row, col, self.__y_channel[r, c]))
        return neighbors
