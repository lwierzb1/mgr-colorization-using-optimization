__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase
import numpy as np
from colorization_program.src.gui.display_canvas import DisplayCanvas


class DisplayCanvasTestCase(TestCase):
    def setUp(self):
        self._display_canvas = DisplayCanvas(None)

    def test_display(self):
        array = np.empty(shape=(240, 320))
        self._display_canvas.display(array)
        np.testing.assert_array_equal(array, self._display_canvas.image_array)

        array = np.random.rand(240, 320)
        self._display_canvas.display(array)
        np.testing.assert_array_equal(array, self._display_canvas.image_array)
