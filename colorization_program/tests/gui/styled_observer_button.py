__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import tkinter as tk
from unittest import TestCase

from colorization_program.src.gui.styled_observer_button import StyledObserverButton
from colorization_program.src.subject.colorization_process import ColorizationProcessSubject


class StyledObserverButtonTestCase(TestCase):
    def setUp(self):
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
