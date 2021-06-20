import tests.context
from unittest import TestCase

from src.observer.colorized_image_observer import ColorizedImageObserver


class ColorizedImageObserverTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
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
