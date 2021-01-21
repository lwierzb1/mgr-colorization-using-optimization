#!/usr/bin/env python
"""
This file is part of Colorization Using Optimization implementation in Python.
Performs colorization.
"""

import numpy as np
from neighbor_solver import NeighborSolver
from optimization_solver import OptimizationSolver
from image_processing_toolkit import bgr_to_yuv_channels, yuv_channels_to_rgb_image
from mathematical_toolkit import compute_variance, ensure_is_not_zero

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def compute_weights_of_y_neighbor_values(neighbor_values, y_value):
    """Computes weights of neighbor pixels for future optimization see:
    https://www.cs.huji.ac.il/~yweiss/Colorization/

    The following formula is used
    .. math::
        w_rs = e^{-(Y(s)-Y(r))^2 / 2\sigma_r^2}
        where r is the index of the center, s the index of a neighbour and
        sigma_r is the variance in a neighbourhood around r.

    neighbor_values: luminance values of neighbor pixels
    y_value: luminance of pixel around which neighbors were searched
    """
    # Calculate variance of neighbor pixels
    variance = compute_variance(neighbor_values)

    # Calculate weight of neighbor pixels
    wrs = np.exp(-((neighbor_values - y_value) ** 2) / variance)

    summed_values = np.sum(wrs)
    # make the weighting function sum up to 1
    wrs = - (wrs / ensure_is_not_zero(summed_values))
    return wrs


class ColorizationSolver:
    def __init__(self, grayscale_bgr_matrix, marked_bgr_matrix):
        self.__grayscale_bgr_matrix = grayscale_bgr_matrix
        self.__marked_bgr_matrix = marked_bgr_matrix
        self.__image_h, self._image_w, _ = grayscale_bgr_matrix.shape
        self.__image_size = self._image_w * self.__image_h

    def solve(self):
        # split to YUV channels
        y_channel, u_channel, v_channel = self.__get_yuv_channels_from_matrices()

        has_hints = abs(self.__grayscale_bgr_matrix - self.__marked_bgr_matrix).sum(2) > 0.01
        wrs = self.__compute_weights(has_hints, y_channel)

        # perform optimization
        optimization_solver = OptimizationSolver(wrs, has_hints)
        new_u, new_v = optimization_solver.optimize(u_channel, v_channel)

        return yuv_channels_to_rgb_image(y_channel, new_u, new_v)

    def __get_yuv_channels_from_matrices(self):
        y_channel, _, _ = bgr_to_yuv_channels(self.__grayscale_bgr_matrix)
        _, u_channel, v_channel = bgr_to_yuv_channels(self.__marked_bgr_matrix)
        return y_channel, u_channel, v_channel

    def __compute_weights(self, has_hints, y_channel):
        wrs = []
        for row in range(self.__image_h):
            for col in range(self._image_w):
                neighbor_solver = NeighborSolver((row, col), y_channel)
                if not has_hints[row][col]:
                    neighbors = neighbor_solver.find_neighbors(wrs)
                    rows, cols, values = zip(*neighbors)
                    weights = compute_weights_of_y_neighbor_values(values, y_channel[row][col])
                    for idx in range(len(weights)):
                        wrs.append((rows[idx], cols[idx], weights[idx]))
                else:
                    r = row * self._image_w + col
                    c = row * self._image_w + col
                    wrs.append((r, c, 1.))
        return wrs
