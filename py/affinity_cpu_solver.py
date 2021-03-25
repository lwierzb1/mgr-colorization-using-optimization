import numpy as np
from numba import jit

from py.affinity_solver import AffinitySolver


class AffinityCpuSolver(AffinitySolver):
    def __init__(self):
        super(AffinitySolver, self).__init__()

    def compute_affinity(self, center_y, neighbors_array):
        sy = neighbors_array[:, 2]
        diff = sy - center_y
        variance = np.var((np.append(sy, center_y)))
        if variance < 1e-7:
            variance = 1e-7
        wrs = np.exp(-(diff ** 2) / variance)
        summed_values = np.sum(wrs)
        # make the weighting function sum up to 1
        wrs = - wrs / summed_values
        neighbors_array[:, 2] = wrs
        return neighbors_array
