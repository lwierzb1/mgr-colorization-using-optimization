from abc import ABC


class WeightsSolver(ABC):
    def __init__(self, neighbor_solver, affinity_solver):
        self._neighbor_solver = neighbor_solver
        self._affinity_solver = affinity_solver

    def compute_wrs(self, has_hints, y_channel):
        pass
