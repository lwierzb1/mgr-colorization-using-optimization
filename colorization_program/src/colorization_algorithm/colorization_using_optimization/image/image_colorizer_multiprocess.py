__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import multiprocessing

import numpy as np

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image import \
    colorization_optimized_solver, abstract_colorizer
from colorization_program.src.config.singleton_config import SingletonConfig

__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


class ImageColorizerMultiprocess(abstract_colorizer.AbstractColorizer):
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
        config = SingletonConfig()

        self._SPLIT_FACTOR = config.processes
        self._colorization_solvers = self._initialize_colorization_solvers()

    def colorize(self):
        results = self._run_solvers_for_result()
        return np.concatenate(results)

    def _run_solvers_for_result(self):
        pool = multiprocessing.Pool(self._SPLIT_FACTOR)
        futures = pool.map(self._run_single_solver_for_result, self._colorization_solvers)
        pool.close()
        pool.join()
        return futures

    @staticmethod
    def _run_single_solver_for_result(solver):
        return solver.solve()

    def _initialize_colorization_solvers(self):
        solvers = []
        grayscale_arrays = np.array_split(self._grayscale_matrix, self._SPLIT_FACTOR)
        marked_arrays = np.array_split(self._marked_matrix, self._SPLIT_FACTOR)
        for i in range(self._SPLIT_FACTOR):
            solvers.append(
                colorization_optimized_solver.ColorizationOptimizedSolver(grayscale_arrays[i], marked_arrays[i], SingletonConfig()))
        return solvers
