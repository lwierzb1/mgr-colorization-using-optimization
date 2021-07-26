__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from unittest import TestCase
from unittest.mock import create_autospec

from colorization_program.src.observer.observer import Observer
from colorization_program.src.subject.colorized_image import ColorizedImageSubject


class PencilConfigSubjectTestCase(TestCase):
    def setUp(self):
        self._colorization_process_subject = ColorizedImageSubject()
        self._observer = create_autospec(spec=Observer)

    def test_update(self):
        self._test_not_attached_observer()
        self._test_attached_observer()

    def _test_not_attached_observer(self):
        self._colorization_process_subject.notify()
        self._observer.update_subject.assert_not_called()

    def _test_attached_observer(self):
        self._colorization_process_subject.attach(self._observer)
        self._colorization_process_subject.notify()
        self._observer.update_subject.assert_called_once()
