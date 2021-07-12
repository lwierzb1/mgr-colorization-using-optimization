import tests.context
from unittest import TestCase
from unittest.mock import create_autospec

from src.observer.observer import Observer
from src.subject.colorization_process import ColorizationProcessSubject


class ColorizationProcessSubjectTestCase(TestCase):
    def setUp(self):
        self._colorization_process_subject = ColorizationProcessSubject()
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
