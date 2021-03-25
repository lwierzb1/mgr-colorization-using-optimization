from abc import ABC
import numpy as np


class NeighborSolver(ABC):
    """
           A class used to solve finding Y channel value of neighbor for given pixel.

           Attributes
           ----------
           __center
               pixel around which we are looking for neighbors

          __WINDOW_WIDTH
               the width of the search window

           Methods
           -------
           find_neighbors(weights)
               Finds neighbors for given pixel.
               If the analyzed pixel is the pixel around which we are looking for neighbors, the weight should be increased
           """

    def __init__(self):
        pass

    def find_neighbors(self, center, y_channel) -> np.array:
        pass
