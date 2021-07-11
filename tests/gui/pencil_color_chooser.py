from unittest import TestCase

import tests.context
from src.gui.pencil_color_chooser import PencilColorChooser
from src.observer.pencil_config_observer import PencilConfigObserver
from src.subject.pencil_config import PencilConfigSubject


class PencilColorChooserTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._config_subject = PencilConfigSubject()
        self._config_observer = PencilConfigObserver()
        self._config_subject.attach(self._config_observer)
        self._pencil_color_chooser = PencilColorChooser(None, self._config_subject)

    def test_apply_color(self):
        self._test_apply_red_color()
        self._test_apply_black_color()

    def _test_apply_black_color(self):
        hex_color_black = '#000000'
        bgr_black = [0, 0, 0]
        self._pencil_color_chooser.apply(hex_color_black)
        self.assertEqual(self._config_observer.hex, hex_color_black)
        self.assertEqual(self._config_observer.bgr, bgr_black)

    def _test_apply_red_color(self):
        hex_color_red = '#ff0000'
        bgr_color_red = [0, 0, 255]
        self._pencil_color_chooser.apply(hex_color_red)
        self.assertEqual(self._config_observer.hex, hex_color_red)
        self.assertEqual(self._config_observer.bgr, bgr_color_red)
