__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase

from colorization_program.src.gui.pencil_color_chooser import PencilColorChooser
from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver
from colorization_program.src.subject.pencil_config import PencilConfigSubject


class PencilColorChooserTestCase(TestCase):
    def setUp(self):
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
