__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import numpy as np


def rgb2yuv(rgb):
    m = np.array([[0.299, 0.587, 0.114],
                  [-0.147, -0.289, 0.436],
                  [0.615, -0.515, -0.100]])

    return np.dot(rgb, m.T.copy())


def yuv2rgb(yiq):
    m = np.array([[1, 0, 1.14],
                  [1, -0.395, -0.581],
                  [1, 2.032, 0]])
    return np.dot(yiq, m.T.copy())
