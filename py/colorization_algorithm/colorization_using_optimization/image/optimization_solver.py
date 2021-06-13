import numpy as np
import scipy
import scipy.sparse as sc_sparse
import scipy.sparse.linalg as sc_linalg

from py.config.singleton_config import SingletonConfig
from py.toolkit import mathematical


class OptimizationSolver:
    """
       A class used to obtain U and V channels based on weights and hints provided by user.

       Attributes
       ----------
       _mat_a
           matrix with weights (https://www.cs.huji.ac.il/~yweiss/Colorization/)

       Methods
       -------
       optimize(u_channel, v_channel)
           Creates new U and V channels for output image based on marked U and V channels.
       """

    def __init__(self, mat_a, has_hints):
        self._mat_a = mat_a
        self._IMAGE_H, self._IMAGE_W = has_hints.shape
        self._IMAGE_SIZE = self._IMAGE_H * self._IMAGE_W
        self._idx_colored = np.nonzero(has_hints.reshape(self._IMAGE_SIZE, order='F'))

    def optimize(self, u_channel, v_channel):
        config = SingletonConfig()
        jacobi_approximation = config.jacobi_approximation
        lin_alg = config.linear_algorithm

        if lin_alg == 'jacobi':
            print('using jacobi', jacobi_approximation)
            # U space solving
            new_u = self._compute_new_color_channel_jacobi(u_channel, jacobi_approximation)
            # V space solving
            new_v = self._compute_new_color_channel_jacobi(v_channel, jacobi_approximation)
            return new_u, new_v
        elif lin_alg == 'lgmres':
            print('using lgmres')
            # U space solving
            new_u = self._compute_new_color_channel_lgmres(u_channel)
            # V space solving
            new_v = self._compute_new_color_channel_lgmres(v_channel)
            return new_u, new_v
        else:
            print('using linalg')
            # U space solving
            new_u = self._compute_new_color_channel(u_channel)
            # V space solving
            new_v = self._compute_new_color_channel(v_channel)
            return new_u, new_v

    def _compute_new_color_channel(self, color_channel):
        b = np.zeros(self._IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self._IMAGE_SIZE, order='F')
        b[self._idx_colored] = pic_channel_flat[self._idx_colored]
        new_color_channel = scipy.sparse.linalg.spsolve(self._mat_a, b)
        return np.reshape(new_color_channel, (self._IMAGE_H, self._IMAGE_W), order='F')

    def _compute_new_color_channel_jacobi(self, color_channel, approximation):
        b = np.zeros(self._IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self._IMAGE_SIZE, order='F')
        b[self._idx_colored] = pic_channel_flat[self._idx_colored]
        new_color_channel = mathematical.jacobi(self._mat_a, b, approximation)
        return np.reshape(new_color_channel, (self._IMAGE_H, self._IMAGE_W), order='F')

    def _compute_new_color_channel_lgmres(self, color_channel):
        b = np.zeros(self._IMAGE_SIZE)
        pic_channel_flat = color_channel.reshape(self._IMAGE_SIZE, order='F')
        b[self._idx_colored] = pic_channel_flat[self._idx_colored]
        new_color_channel, _ = sc_linalg.lgmres(self._mat_a, b)
        return np.reshape(new_color_channel, (self._IMAGE_H, self._IMAGE_W), order='F')
