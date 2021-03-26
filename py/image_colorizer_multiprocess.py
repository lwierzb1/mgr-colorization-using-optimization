#!/usr/bin/env python
from multiprocessing import Pool

import numpy as np

from abstract_colorizer import AbstractColorizer
from py.colorization_solver import ColorizationSolver
from py.image_processing_toolkit import rgb_matrix_to_image

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def _run_single_solver_for_result(solver):
    result = solver.solve()
    return rgb_matrix_to_image(result)


class ImageColorizerMultiprocess(AbstractColorizer):
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
        self.__colorization_solvers = self.__initialize_colorization_solvers(4)

    def colorize(self):
        results = self.__run_solvers_for_result()
        return np.concatenate(results)

    def __run_solvers_for_result(self):
        pool = Pool()
        futures = pool.map(_run_single_solver_for_result, self.__colorization_solvers)
        pool.close()
        pool.join()
        return futures

    def __initialize_colorization_solvers(self, number_of_splits):
        solvers = []
        grayscale_arrays = np.array_split(self._grayscale_matrix, number_of_splits)
        marked_arrays = np.array_split(self._marked_matrix, number_of_splits)
        for i in range(number_of_splits):
            solvers.append(ColorizationSolver(grayscale_arrays[i], marked_arrays[i]))
        return solvers
