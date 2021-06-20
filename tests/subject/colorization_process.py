import tests.context
from unittest import TestCase
from unittest.mock import MagicMock

from src.observer.observer import Observer
from src.subject.colorization_process import ColorizationProcessSubject



class ColorizationProcessSubjectTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._colorization_process_subject = ColorizationProcessSubject()

    def test_update(self):
        observer = Observer()
        observer.update_subject = MagicMock()

        self._colorization_process_subject.notify()
        observer.update_subject.assert_not_called()

        self._colorization_process_subject.attach(observer)
        self._colorization_process_subject.notify()
        observer.update_subject.assert_called_once()
