#!/usr/bin/env python

from abstract_colorizer import AbstractColorizer
from colorization_solver import ColorizationSolver
from colorization_optimized_solver import ColorizationOptimizedSolver

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


class ImageColorizer(AbstractColorizer):
    """
    A class used to represent an Image implementation of abstract colorizer.
    The grayscale image and marked image files provides the input data to colorization algorithm.

    ...

    Attributes
    ----------

    Methods
    -------
    colorize()
        Colorizes grayscale image and store it.
    """

    def __init__(self, grayscale, marked):
        super().__init__(grayscale, marked)
        self.__colorization_solver = ColorizationSolver(self._grayscale_matrix, self._marked_matrix)

    def colorize(self):
        return self.__colorization_solver.solve()
