import tests.context
from unittest import TestCase
from src.gui.pencil_width_picker import PencilWidthPicker
from src.observer.pencil_config_observer import PencilConfigObserver
from src.subject.pencil_config import PencilConfigSubject


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
