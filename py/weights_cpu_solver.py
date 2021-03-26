from py.affinity_cpu_solver import AffinityCpuSolver
from py.neighbor_cpu_solver import NeighborCpuSolver
from py.weights_solver import WeightsSolver


def _to_seq(r, c, rows):
    return c * rows + r


class WeightsCpuSolver(WeightsSolver):
    def __init__(self):
        super().__init__(NeighborCpuSolver(), AffinityCpuSolver())

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
                        wrs.append([_to_seq(row, col, height), _to_seq(neighbors[idx][0], neighbors[idx][1], height),
                                    weights[idx]])
                wrs.append([_to_seq(row, col, height), _to_seq(row, col, height), 1.])
        return wrs
