from unittest import TestCase
import tests.context
import numpy as np
from src.gui.display_canvas import DisplayCanvas


class DisplayCanvasTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._display_canvas = DisplayCanvas(None)

    def test_display(self):
        array = np.empty(shape=(240, 320))
        self._display_canvas.display(array)
        np.testing.assert_array_equal(array, self._display_canvas.image_array)

        array = np.random.rand(240, 320)
        self._display_canvas.display(array)
        np.testing.assert_array_equal(array, self._display_canvas.image_array)
