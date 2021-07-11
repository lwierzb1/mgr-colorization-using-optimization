import tests.context
from unittest import TestCase
import tkinter as tk
from unittest import mock
from src.behaviour.draw_behaviour import DrawBehaviour
from src.subject.pencil_config import PencilConfigSubject


class DrawBehaviourTestCase(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._canvas = tk.Canvas()
        self._pencil_config = PencilConfigSubject()
        self._draw_behaviour = DrawBehaviour(self._canvas, self._pencil_config)

    def test_draw_dot(self):
        click_event = self._create_mock_click(100, 100)
        self._draw_behaviour.draw_dot(click_event)
        self.assertEqual(len(self._draw_behaviour.executed_commands), 1)

    def test_undo_last_command(self):
        click_event = self._create_mock_click(100, 100)
        self._draw_behaviour.draw_dot(click_event)
        self.assertEqual(len(self._draw_behaviour.executed_commands), 1)
        self._draw_behaviour.undo_last_command()
        self.assertEqual(len(self._draw_behaviour.executed_commands), 0)

    def test_redo_last_command(self):
        click_event = self._create_mock_click(100, 100)
        self._draw_behaviour.draw_dot(click_event)
        self.assertEqual(len(self._draw_behaviour.executed_commands), 1)
        self._draw_behaviour.undo_last_command()
        self.assertEqual(len(self._draw_behaviour.executed_commands), 0)
        self._draw_behaviour.redo_last_command()
        self.assertEqual(len(self._draw_behaviour.executed_commands), 1)

    @staticmethod
    def _create_mock_click(x, y):
        event = mock.Mock()
        event.x = x
        event.y = y
        return event

