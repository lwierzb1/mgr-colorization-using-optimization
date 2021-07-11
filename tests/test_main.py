#!/usr/bin/env python3
import context
import unittest

from tests.behaviour.draw_behaviour import DrawBehaviourTestCase
from tests.command.line_drawing_command import LineDrawingCommandTestCase
from tests.gui.display_canvas import DisplayCanvasTestCase
from tests.gui.pencil_color_chooser import PencilColorChooserTestCase
from tests.gui.pencil_width_picker import PencilWidthPickerTestCase
from tests.gui.styled_observer_button import StyledObserverButtonTestCase
from tests.observer.colorized_image_observer import ColorizedImageObserverTestCase
from tests.observer.pencil_config_observer import PencilConfigObserverTestCase
from tests.subject.colorization_process import ColorizationProcessSubjectTestCase
from tests.subject.pencil_config import PencilConfigSubjectTestCase
from tests.toolkit.image_processing_toolkit import ImageProcessingToolkitTestCase


def test_suite_image_processing_toolkit():
    image_processing_toolkit_test_case = ImageProcessingToolkitTestCase()
    image_processing_toolkit_test_case.test_hex_to_bgr()


def test_suite_colorized_image_observer():
    colorized_image_observer = ColorizedImageObserverTestCase()
    colorized_image_observer.test_update_subject()


def test_suite_pencil_config_observer():
    pencil_config_observer = PencilConfigObserverTestCase()
    pencil_config_observer.test_update_subject()


def test_suite_colorization_process_subject():
    colorization_process_subject = ColorizationProcessSubjectTestCase()
    colorization_process_subject.test_update()


def test_suite_pencil_config_subject():
    colorization_process_subject = PencilConfigSubjectTestCase()
    colorization_process_subject.test_update()


def test_suite_display_canvas():
    colorization_process_subject = DisplayCanvasTestCase()
    colorization_process_subject.test_display()


def test_suite_pencil_width_picker():
    pencil_width_picker = PencilWidthPickerTestCase()
    pencil_width_picker.test_width_apply()


def test_suite_pencil_color_chooser():
    pencil_color_chooser = PencilColorChooserTestCase()
    pencil_color_chooser.test_apply_color()


def test_suite_styled_button():
    styled_button = StyledObserverButtonTestCase()
    styled_button.test_state_update_by_colorization_process_subject()


def test_draw_behaviour():
    draw_behaviour = DrawBehaviourTestCase()
    draw_behaviour.test_draw_dot()
    draw_behaviour.test_undo_last_command()
    draw_behaviour.test_redo_last_command()


def test_suite_line_drawing_command():
    line_drawing_command = LineDrawingCommandTestCase()
    line_drawing_command.test_draw_line()


if __name__ == '__main__':
    unittest.main()
