#!/usr/bin/env python
import cv2

from abstract_colorizer import AbstractColorizer
from image_processing_toolkit import rgb_matrix_to_image

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
    __destination:
        path to the colored file

    Methods
    -------
    colorize()
        Colorizes grayscale image and store it.
    """

    def __init__(self, grayscale, marked, destination):
        super().__init__(grayscale, marked)
        self.__destination = destination

    def colorize(self):
        result = self._colorization_solver.solve()
        result = rgb_matrix_to_image(result)
        # show_result(result)
        self.__store_result(result)

    def __store_result(self, result):
        cv2.imwrite(self.__destination, result)


def show_result(result):
    print("Press [esc] to close result window...")
    while True:
        cv2.imshow("result", result)
        k = cv2.waitKey(33)
        if k == 27:  # Esc key to stop
            break
