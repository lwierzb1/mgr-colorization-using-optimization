__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from abc import ABC


class AffinitySolver(ABC):
    def compute_affinity(self, center_y, neighbors_y):
        pass
