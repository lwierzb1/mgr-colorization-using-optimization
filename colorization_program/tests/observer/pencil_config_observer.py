__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase

from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver


class PencilConfigObserverTestCase(TestCase):
    def setUp(self) -> None:
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
