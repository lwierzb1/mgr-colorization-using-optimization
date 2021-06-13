from abc import ABC

from py.toolkit import image_processing

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


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
        self._grayscale_matrix = image_processing.bgr_as_float_matrix(grayscale)
        self._marked_matrix = image_processing.bgr_as_float_matrix(marked)

    def colorize(self):
        pass
