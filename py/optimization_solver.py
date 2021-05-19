#!/usr/bin/env python


import numpy as np
import scipy
from scipy.sparse import linalg
from scipy.sparse.linalg import lgmres, cg
from mathematical_toolkit import jacobi
import sys

from singleton_config import SingletonConfig


class OptimizationSolver:
    """
       A class used to obtain U and V channels based on weights and hints provided by user.

       Attributes
       ----------
       __mat_a
           matrix with weights (https://www.cs.huji.ac.il/~yweiss/Colorization/)

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
        config = SingletonConfig()
        jacobi_approximation = config.jacobi_approximation
        lin_alg = config.linear_algorithm

        if lin_alg == 'jacobi':
            print('using jacobi', jacobi_approximation)
            # U space solving
            new_u = self.__compute_new_color_channel_jacobi(u_channel, jacobi_approximation)
            # V space solving
            new_v = self.__compute_new_color_channel_jacobi(v_channel, jacobi_approximation)
            return new_u, new_v
        elif lin_alg == 'lgmres':
            print('using lgmres')
            # U space solving
            new_u = self.__compute_new_color_channel_lgmres(u_channel)
            # V space solving
            new_v = self.__compute_new_color_channel_lgmres(v_channel)
            return new_u, new_v
        else:
            print('using linalg')
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
        new_color_channel = jacobi(self.__mat_a, b, approximation)
        return np.reshape(new_color_channel, (self.__IMAGE_H, self.__IMAGE_W), order='F')

    def __compute_new_color_channel_lgmres(self, color_channel):
        b = np.zeros(self.__IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self.__IMAGE_SIZE, order='F')
        b[self.__idx_colored] = pic_channel_flat[self.__idx_colored]
        new_color_channel, _ = lgmres(self.__mat_a, b)
        return np.reshape(new_color_channel, (self.__IMAGE_H, self.__IMAGE_W), order='F')
