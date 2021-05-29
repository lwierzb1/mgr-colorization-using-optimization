#!/usr/bin/env python
from abc import ABC

import cv2

from colorization_solver import ColorizationSolver

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from image_processing_toolkit import bgr_as_float_matrix, read_image, gaussian_blur


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
        # bgr_grayscale = read_image(grayscale)
        # bgr_marked = read_image(marked)
        self._grayscale_matrix = bgr_as_float_matrix(grayscale)
        self._marked_matrix = bgr_as_float_matrix(marked)

    def colorize(self):
        pass
