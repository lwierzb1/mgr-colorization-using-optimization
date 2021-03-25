#!/usr/bin/env python
import numpy as np
import scipy.sparse

from image_processing_toolkit import bgr_to_yuv_channels, yuv_channels_to_bgr_image
from mathematical_toolkit import compute_variance, ensure_is_not_zero
from optimization_solver import OptimizationSolver
import time
__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from py.weights_cpu_solver import WeightsCpuSolver

from py.weights_gpu_solver import WeightsGpuSolver


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
        self._weights_solver = WeightsGpuSolver()

    def solve(self):
        # split to YUV channels
        y_channel, u_channel, v_channel = self.__get_yuv_channels_from_matrices()
        has_hints = abs(self.__grayscale_bgr_matrix - self.__marked_bgr_matrix).sum(2) > 0.01
        s = time.time()
        wrs = self._weights_solver.compute_wrs(has_hints, y_channel)
        s1 = time.time()
        print(s-s1)
        mat_a = self.__map_wrs_to_sparse_matrix(wrs)
        print(s1-time.time())
        # perform optimization
        optimization_solver = OptimizationSolver(mat_a, has_hints)

        new_u, new_v = optimization_solver.optimize(u_channel, v_channel)
        return yuv_channels_to_bgr_image(y_channel, new_u, new_v)

    def __get_yuv_channels_from_matrices(self):
        y_channel, _, _ = bgr_to_yuv_channels(self.__grayscale_bgr_matrix)
        _, u_channel, v_channel = bgr_to_yuv_channels(self.__marked_bgr_matrix)
        return y_channel, u_channel, v_channel

    def to_seq(self, r, c, rows):
        return c * rows + r

    def __map_wrs_to_sparse_matrix(self, wrs):
        sp_idx_rc_data = [
            [self.to_seq(e[0][0], e[0][1], self.__IMAGE_H), self.to_seq(e[1][0], e[1][1], self.__IMAGE_H), e[2]] for e
            in wrs]
        sp_idx_rc = np.array(sp_idx_rc_data, dtype=np.integer)[:, 0:2]
        sp_data = np.array(sp_idx_rc_data, dtype=np.float32)[:, 2]

        return scipy.sparse.csr_matrix((sp_data, (sp_idx_rc[:, 0], sp_idx_rc[:, 1])),
                                       shape=(self.__IMAGE_SIZE, self.__IMAGE_SIZE))
