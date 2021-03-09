#!/usr/bin/env python


import numpy as np
import scipy
from scipy.sparse import linalg
from mathematical_toolkit import jacobi


class OptimizationSolver:
    """
       A class used to obtain U and V channels based on weights and hints provided by user.

       Attributes
       ----------
       __A
           matrix with weights (https://www.cs.huji.ac.il/~yweiss/Colorization/)

      __b
           matrix created based on user provided hints

       Methods
       -------
       optimize(u_channel, v_channel)
           Creates new U and V channels for output image based on marked U and V channels.
       """

    def __init__(self, wrs, has_hints):
        self.__wrs = wrs
        self.__has_hints = has_hints
        self.__IMAGE_H, self.__IMAGE_W = has_hints.shape
        self.__IMAGE_SIZE = self.__IMAGE_H * self.__IMAGE_W

        row_idx, col_idx, wrs_value = zip(*self.__wrs)
        self.__A = scipy.sparse.csr_matrix((wrs_value, (row_idx, col_idx)),
                                           (self.__IMAGE_SIZE, self.__IMAGE_SIZE))
        self.__b = np.zeros((self.__A.shape[0]))

    def optimize(self, u_channel, v_channel):
        color_copy_for_nonzero = self.__has_hints.reshape(self.__IMAGE_SIZE).copy()
        colored_idx = np.nonzero(color_copy_for_nonzero)

        # U space solving
        new_u = self.__compute_new_color_channel_jacobi(u_channel, colored_idx)
        # V space solving
        new_v = self.__compute_new_color_channel_jacobi(v_channel, colored_idx)

        return new_u, new_v

    def __compute_new_color_channel(self, color_channel, colored_idx):
        color_channel_image = color_channel.reshape(self.__IMAGE_SIZE)
        self.__b[colored_idx] = color_channel_image[colored_idx]
        new_color_channel = linalg.spsolve(self.__A, self.__b)
        return new_color_channel.reshape((self.__IMAGE_H, self.__IMAGE_W))

    def __compute_new_color_channel_jacobi(self, color_channel, colored_idx):
        color_channel_image = color_channel.reshape(self.__IMAGE_SIZE)
        self.__b[colored_idx] = color_channel_image[colored_idx]
        new_color_channel = jacobi(self.__A, self.__b, np.zeros(self.__A.shape[0]), 700)
        return new_color_channel.reshape((self.__IMAGE_H, self.__IMAGE_W))
