import numba
import numpy as np

import affinity_solver


class AffinityOptimizedSolver(affinity_solver.AffinitySolver):
    def __init__(self):
        super(affinity_solver.AffinitySolver, self).__init__()

    def compute_affinity(self, center_y, neighbors):
        return _compute_affinity_optimized(center_y, neighbors)


@numba.jit(nopython=True, cache=True, fastmath=True, nogil=True)
def _compute_affinity_optimized(center_y, neighbors_y):
    diff = neighbors_y - center_y
    variance = np.var((np.append(neighbors_y, center_y)))
    if variance < 1e-7:
        variance = 1e-7
    wrs = np.exp(-(diff ** 2) / variance)
    summed_values = np.sum(wrs)
    # make the weighting function sum up to 1
    wrs = - wrs / summed_values
    return wrs
