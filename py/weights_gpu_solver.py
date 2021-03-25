from py.affinity_gpu_solver import AffinityGpuSolver
from py.neighbor_gpu_solver import NeighborGpuSolver
from py.weights_solver import WeightsSolver


class WeightsGpuSolver(WeightsSolver):
    def __init__(self):
        super().__init__(NeighborGpuSolver(), AffinityGpuSolver())

    def compute_wrs(self, has_hints, y_channel):
        height = has_hints.shape[0]
        width = has_hints.shape[1]
        wrs = []
        for row in range(height):
            for col in range(width):
                if not has_hints[row][col]:
                    neighbors = self._neighbor_solver.find_neighbors((row, col), y_channel)
                    weights = self._affinity_solver.compute_affinity(y_channel[(row, col)], neighbors[:, 2])
                    for idx in range(len(weights)):
                        wrs.append([(row, col), (neighbors[idx][0], neighbors[idx][1]), weights[idx]])
                wrs.append([(row, col), (row, col), 1.])
        return wrs
