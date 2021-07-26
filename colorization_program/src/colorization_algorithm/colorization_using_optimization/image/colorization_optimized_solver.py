__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import time

import numpy as np
import scipy.sparse

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.optimization_solver import OptimizationSolver
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.weights_optimized_solver import \
    WeightsOptimizedSolver
from colorization_program.src.config.singleton_config import SingletonConfig
from colorization_program.src.toolkit import mathematical as mtk, image_processing


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
    variance = mtk.compute_variance(neighbor_values)

    # Calculate weight of neighbor pixels
    wrs = np.exp(-((neighbor_values - y_value) ** 2) / variance)

    summed_values = np.sum(wrs)
    # make the weighting function sum up to 1
    wrs = - (wrs / mtk.ensure_is_not_zero(summed_values))
    return wrs


class ColorizationOptimizedSolver:
    """
       A class used to solve Colorization problem. Using OptimizationSolver to colorize image.
       Gets grayscale and marked matrices in BGR space, returns colorized image in BGR space.
       """

    def __init__(self, grayscale_bgr_matrix, marked_bgr_matrix, config):
        self._grayscale_bgr_matrix = grayscale_bgr_matrix
        self._marked_bgr_matrix = marked_bgr_matrix
        self._IMAGE_H, self._IMAGE_W, _ = grayscale_bgr_matrix.shape
        self._IMAGE_SIZE = self._IMAGE_W * self._IMAGE_H
        self._weights_solver = WeightsOptimizedSolver()
        self._config = config

    def solve(self):
        # split to YUV channels
        y_channel, u_channel, v_channel = self._get_yuv_channels_from_matrices()
        has_hints = abs(self._grayscale_bgr_matrix - self._marked_bgr_matrix).sum(2) > 0.01
        s = time.time()
        image_coordinates, neighbors_coordinates, wrs = self._weights_solver.compute_wrs(has_hints, y_channel)
        s1 = time.time()
        print('weights took: ', s1 - s)
        mat_a = self._map_wrs_to_sparse_matrix(image_coordinates, neighbors_coordinates, wrs)
        s2 = time.time()
        print('mapping to sparse took: ', s2 - s1)
        # perform optimization
        solver = OptimizationSolver(mat_a, has_hints, self._config)

        s3 = time.time()
        new_u, new_v = solver.optimize(u_channel, v_channel)
        print('optimize: ', time.time() - s3)
        return image_processing.yuv_channels_to_bgr_matrix(y_channel, new_u, new_v)

    def _get_yuv_channels_from_matrices(self):
        y_channel, _, _ = image_processing.bgr_to_yuv_channels(self._grayscale_bgr_matrix)
        _, u_channel, v_channel = image_processing.bgr_to_yuv_channels(self._marked_bgr_matrix)

        return y_channel, u_channel, v_channel

    def _map_wrs_to_sparse_matrix(self, image_coordinates, neighbors_coordinates, wrs):
        return scipy.sparse.csr_matrix((wrs, (image_coordinates, neighbors_coordinates)),
                                       shape=(self._IMAGE_SIZE, self._IMAGE_SIZE))
