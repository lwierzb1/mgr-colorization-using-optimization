__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from abc import ABC

from colorization_program.src.toolkit import image_processing


class AbstractColorizer(ABC):
    def __init__(self, grayscale, marked):
        self._grayscale_matrix = image_processing.bgr_as_float_matrix(grayscale)
        self._marked_matrix = image_processing.bgr_as_float_matrix(marked)

    def colorize(self):
        pass
