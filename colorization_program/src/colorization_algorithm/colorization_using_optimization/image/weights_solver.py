__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from abc import ABC


class WeightsSolver(ABC):
    def __init__(self, neighbor_solver, affinity_solver):
        self._neighbor_solver = neighbor_solver
        self._affinity_solver = affinity_solver

    def compute_wrs(self, has_hints, y_channel):
        pass
