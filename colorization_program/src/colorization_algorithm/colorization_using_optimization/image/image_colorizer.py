__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image import colorization_solver, \
    abstract_colorizer


class ImageColorizer(abstract_colorizer.AbstractColorizer):
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
        self._colorization_solver = colorization_solver.ColorizationSolver(self._grayscale_matrix, self._marked_matrix)

    def colorize(self):
        return self._colorization_solver.solve()
