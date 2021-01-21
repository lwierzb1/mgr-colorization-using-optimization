#!/usr/bin/env python
"""This file is part of Colorization Using Optimization implementation in Python.
Performs optimization process.
Ax=b
A- wrs matrix
b- vector with u,v values
"""

import numpy as np
import scipy
from scipy.sparse import linalg


class OptimizationSolver:
    def __init__(self, wrs, has_hints):
        self.__wrs = wrs
        self.__has_hints = has_hints
        self.__image_h, self._image_w = has_hints.shape
        self.__image_size = self.__image_h * self._image_w

        row_idx, col_idx, wrs_value = zip(*self.__wrs)
        self.__A = scipy.sparse.csr_matrix((wrs_value, (row_idx, col_idx)),
                                           (self.__image_size, self.__image_size))
        self.__b = np.zeros((self.__A.shape[0]))

    def optimize(self, u_channel, v_channel):
        color_copy_for_nonzero = self.__has_hints.reshape(self.__image_size).copy()
        colored_idx = np.nonzero(color_copy_for_nonzero)

        # U space solving
        new_u = self.__compute_new_color_channel(u_channel, colored_idx)
        # V space solving
        new_v = self.__compute_new_color_channel(v_channel, colored_idx)

        return new_u, new_v

    def __compute_new_color_channel(self, color_channel, colored_idx):
        color_channel_image = color_channel.reshape(self.__image_size)
        self.__b[colored_idx] = color_channel_image[colored_idx]
        new_color_channel = linalg.spsolve(self.__A, self.__b)
        return new_color_channel.reshape((self.__image_h, self._image_w))
