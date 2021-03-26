#!/usr/bin/env python
"""General purpose mathematical functions.
"""

import numpy as np
import scipy.sparse as sc
from numba import jit

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


@jit(nopython=True, fastmath=True, cache=True, nogil=True)
def compute_variance(values):
    """Returns the variance from the given set.

    values: values from which the variance is to be calculated
    """
    # Calculate variance
    variance = np.var(values)
    return ensure_is_not_zero(variance)


@jit(nopython=True, fastmath=True, cache=True, nogil=True)
def ensure_is_not_zero(number):
    # avoid dividing by "0"
    if number < 1e-6:
        number = 1e-6
    return number


def jacobi(A, b, x, n):
    D = A.diagonal()
    R = A - sc.diags(D)
    for i in range(n):
        x = (b - R.dot(x)) / D
    return x


@jit(nopython=True, fastmath=True, cache=True, nogil=True)
def to_seq(r, c, rows):
    return c * rows + r
