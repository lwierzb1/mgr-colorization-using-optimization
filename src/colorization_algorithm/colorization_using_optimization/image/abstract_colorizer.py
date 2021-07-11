from abc import ABC

from src.toolkit import image_processing


class AbstractColorizer(ABC):
    def __init__(self, grayscale, marked):
        self._grayscale_matrix = image_processing.bgr_as_float_matrix(grayscale)
        self._marked_matrix = image_processing.bgr_as_float_matrix(marked)

    def colorize(self):
        pass
