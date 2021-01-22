#!/usr/bin/env python
from abc import ABC

from colorization_solver import ColorizationSolver

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from image_processing_toolkit import read_as_float_matrix


class AbstractColorizer(ABC):
    """
    A class used to represent an abstract colorizer.

    ...

    Attributes
    ----------
    _colorization_solver : ColorizationSolver
        object solving colorization problem

    Methods
    -------
    colorize()
        Abstract method.
        Runs colorization process.
    """

    def __init__(self, grayscale, marked):
        self._grayscale_matrix = read_as_float_matrix(grayscale)
        self._marked_matrix = read_as_float_matrix(marked)
        self._colorization_solver = ColorizationSolver(self._grayscale_matrix, self._marked_matrix)

    def colorize(self):
        pass
