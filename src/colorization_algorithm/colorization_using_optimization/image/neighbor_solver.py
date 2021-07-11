import abc

import numpy as np


class NeighborSolver(abc.ABC):
    def __init__(self):
        pass

    def find_neighbors(self, center, y_channel) -> np.array:
        pass
