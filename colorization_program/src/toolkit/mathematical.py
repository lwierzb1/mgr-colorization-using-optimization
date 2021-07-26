__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

"""General purpose mathematical functions.
"""

import numba
import numpy as np
import scipy.sparse as sc


@numba.jit(nopython=True, fastmath=True, cache=True, nogil=True)
def compute_variance(values):
    """Returns the variance from the given set.

    values: values from which the variance is to be calculated
    """
    # Calculate variance
    variance = np.var(values)
    return ensure_is_not_zero(variance)


@numba.jit(nopython=True, fastmath=True, cache=True, nogil=True)
def ensure_is_not_zero(number):
    # avoid dividing by "0"
    if number < 1e-6:
        number = 1e-6
    return number


def jacobi(A, b, n, tol=1e-3):
    x = np.zeros(A.shape[0])
    D = A.diagonal()
    R = A - sc.diags(D)
    i = 0
    while True:
        xk = (b - R.dot(x)) / D
        norm = np.linalg.norm(xk - x)
        if norm < tol or i > n:
            break
        else:
            x = xk
            i += 1
    return x


@numba.jit(nopython=True, fastmath=True, cache=True, nogil=True)
def to_seq(r, c, rows):
    return c * rows + r
