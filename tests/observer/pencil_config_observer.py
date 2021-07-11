import tests.context
from unittest import TestCase

from src.observer.pencil_config_observer import PencilConfigObserver


class PencilConfigObserverTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._image_observer = PencilConfigObserver()

    def test_update_subject(self):
        width = 100
        hex_color = '#000000'
        bgr = [0, 0, 0]
        self._update_image_observer(width=width, hex=hex_color, bgr=bgr)
        self._assert_equal_properties(width=width, hex=hex_color, bgr=bgr)

    def _assert_equal_properties(self, **kwargs):
        self.assertEqual(self._image_observer.width, kwargs.get('width'))
        self.assertEqual(self._image_observer.hex, kwargs.get('hex'))
        self.assertEqual(self._image_observer.bgr, kwargs.get('bgr'))

    def _update_image_observer(self, **kwargs):
        self._image_observer.update_subject(**kwargs)
