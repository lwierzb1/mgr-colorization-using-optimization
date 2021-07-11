import tests.context
import tkinter as tk
from unittest import TestCase

from src.gui.styled_observer_button import StyledObserverButton
from src.subject.colorization_process import ColorizationProcessSubject


class StyledObserverButtonTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._subject = ColorizationProcessSubject()
        self._button = StyledObserverButton()
        self._subject.attach(self._button)

    def test_state_update_by_colorization_process_subject(self):
        self._test_normal_state()

        self._disable_button()
        self._test_disabled_state()

        self._enable_button()
        self._test_normal_state()

    def _disable_button(self):
        self._subject.notify(start=False)

    def _enable_button(self):
        self._subject.notify(start=True)

    def _test_disabled_state(self):
        self._test_state(tk.DISABLED)

    def _test_normal_state(self):
        self._test_state(tk.NORMAL)

    def _test_state(self, state):
        self.assertEqual(state, str(self._button['state']))
