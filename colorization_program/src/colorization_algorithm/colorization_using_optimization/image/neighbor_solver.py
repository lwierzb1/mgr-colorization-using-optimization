__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import abc

import numpy as np


class NeighborSolver(abc.ABC):
    def __init__(self):
        pass

    def find_neighbors(self, center, y_channel) -> np.array:
        pass
