#!/usr/bin/env python


import numpy as np
import scipy
from scipy.sparse import linalg
from mathematical_toolkit import jacobi
import sys


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

    def __init__(self, mat_a, has_hints):
        self.__mat_a = mat_a
        self.__IMAGE_H, self.__IMAGE_W = has_hints.shape
        self.__IMAGE_SIZE = self.__IMAGE_H * self.__IMAGE_W
        self.__idx_colored = np.nonzero(has_hints.reshape(self.__IMAGE_SIZE, order='F'))

    def optimize(self, u_channel, v_channel):
        approximation = int(sys.argv[8])

        if approximation > 0:
            # U space solving
            new_u = self.__compute_new_color_channel_jacobi(u_channel, approximation)
            # V space solving
            new_v = self.__compute_new_color_channel_jacobi(v_channel, approximation)
            return new_u, new_v
        else:
            # U space solving
            new_u = self.__compute_new_color_channel(u_channel)
            # V space solving
            new_v = self.__compute_new_color_channel(v_channel)
            return new_u, new_v

    def __compute_new_color_channel(self, color_channel):
        b = np.zeros(self.__IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self.__IMAGE_SIZE, order='F')
        b[self.__idx_colored] = pic_channel_flat[self.__idx_colored]
        new_color_channel = scipy.sparse.linalg.spsolve(self.__mat_a, b)
        return np.reshape(new_color_channel, (self.__IMAGE_H, self.__IMAGE_W), order='F')

    def __compute_new_color_channel_jacobi(self, color_channel, approximation):
        b = np.zeros(self.__IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self.__IMAGE_SIZE, order='F')
        b[self.__idx_colored] = pic_channel_flat[self.__idx_colored]
        new_color_channel = jacobi(self.__mat_a, b, np.zeros(self.__mat_a.shape[0]), approximation)
        return np.reshape(new_color_channel, (self.__IMAGE_H, self.__IMAGE_W), order='F')
