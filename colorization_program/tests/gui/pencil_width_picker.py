__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase
from colorization_program.src.gui.pencil_width_picker import PencilWidthPicker
from colorization_program.src.observer.pencil_config_observer import PencilConfigObserver
from colorization_program.src.subject.pencil_config import PencilConfigSubject


class PencilWidthPickerTestCase(TestCase):
    def test_width_apply(self):
        config_subject = PencilConfigSubject()
        config_observer = PencilConfigObserver()
        config_subject.attach(config_observer)

        width = 100
        radius = width / 2
        width_picker = PencilWidthPicker(None, config_subject)
        width_picker.apply(width)

        self.assertEqual(radius, float(config_observer.width))
