__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase

from colorization_program.src.observer.colorized_image_observer import ColorizedImageObserver


class ColorizedImageObserverTestCase(TestCase):
    def setUp(self):
        self._image_observer = ColorizedImageObserver()

    def test_update_subject(self):
        x_start = 1
        y_start = 0
        result = []
        self._update_image_observer(x_start=x_start, y_start=y_start, result=result)
        self._assert_equal_properties(x_start=x_start, y_start=y_start, result=result)

    def _assert_equal_properties(self, **kwargs):
        self.assertEqual(self._image_observer.x_start, kwargs.get('x_start'))
        self.assertEqual(self._image_observer.y_start, kwargs.get('y_start'))
        self.assertEqual(self._image_observer.result, kwargs.get('result'))

    def _update_image_observer(self, **kwargs):
        self._image_observer.update_subject(**kwargs)
