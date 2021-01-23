#!/usr/bin/env python
"""General purpose mathematical functions.
"""

import numpy as np

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def compute_variance(values):
    """Returns the variance from the given set.

    values: values from which the variance is to be calculated
    """
    # Calculate variance
    variance = np.var(values)
    return ensure_is_not_zero(variance)


def ensure_is_not_zero(number):
    # avoid dividing by "0"
    if number < 1e-6:
        number = 1e-6
    return number
