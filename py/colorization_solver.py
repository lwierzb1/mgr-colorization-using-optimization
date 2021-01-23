#!/usr/bin/env python
import numpy as np

from image_processing_toolkit import bgr_to_yuv_channels, yuv_channels_to_bgr_image
from mathematical_toolkit import compute_variance, ensure_is_not_zero
from neighbor_solver import NeighborSolver
from optimization_solver import OptimizationSolver

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
    """
       A class used to solve Colorization problem. Using OptimizationSolver to colorize image.
       Gets grayscale and marked matrices in BGR space, returns colorized image in BGR space.

       Attributes
       ----------
       __grayscale_bgr_matrix
           instance of CNN neural network

       Methods
       -------
       solve()
           Colorizes input grayscale image using CNN.
       """

    def __init__(self, grayscale_bgr_matrix, marked_bgr_matrix):
        self.__grayscale_bgr_matrix = grayscale_bgr_matrix
        self.__marked_bgr_matrix = marked_bgr_matrix
        self.__IMAGE_H, self._IMAGE_W, _ = grayscale_bgr_matrix.shape
        self.__IMAGE_SIZE = self._IMAGE_W * self.__IMAGE_H

    def solve(self):
        # split to YUV channels
        y_channel, u_channel, v_channel = self.__get_yuv_channels_from_matrices()

        has_hints = abs(self.__grayscale_bgr_matrix - self.__marked_bgr_matrix).sum(2) > 0.01
        wrs = self.__compute_weights(has_hints, y_channel)

        # perform optimization
        optimization_solver = OptimizationSolver(wrs, has_hints)
        new_u, new_v = optimization_solver.optimize(u_channel, v_channel)

        return yuv_channels_to_bgr_image(y_channel, new_u, new_v)

    def __get_yuv_channels_from_matrices(self):
        y_channel, _, _ = bgr_to_yuv_channels(self.__grayscale_bgr_matrix)
        _, u_channel, v_channel = bgr_to_yuv_channels(self.__marked_bgr_matrix)
        return y_channel, u_channel, v_channel

    def __compute_weights(self, has_hints, y_channel):
        wrs = []
        for row in range(self.__IMAGE_H):
            for col in range(self._IMAGE_W):
                neighbor_solver = NeighborSolver((row, col), y_channel)
                if not has_hints[row][col]:
                    neighbors = neighbor_solver.find_neighbors(wrs)
                    rows, cols, values = zip(*neighbors)
                    weights = compute_weights_of_y_neighbor_values(values, y_channel[row][col])
                    for idx in range(len(weights)):
                        wrs.append((rows[idx], cols[idx], weights[idx]))
                else:
                    r = row * self._IMAGE_W + col
                    c = row * self._IMAGE_W + col
                    wrs.append((r, c, 1.))
        return wrs
