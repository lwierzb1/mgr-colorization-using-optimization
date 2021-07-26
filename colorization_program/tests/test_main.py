#!/usr/bin/env python
__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import unittest

from colorization_program.tests.behaviour.draw_behaviour import DrawBehaviourTestCase
from colorization_program.tests.command.line_drawing_command import LineDrawingCommandTestCase
from colorization_program.tests.gui.display_canvas import DisplayCanvasTestCase
from colorization_program.tests.gui.pencil_color_chooser import PencilColorChooserTestCase
from colorization_program.tests.gui.pencil_width_picker import PencilWidthPickerTestCase
from colorization_program.tests.gui.styled_observer_button import StyledObserverButtonTestCase
from colorization_program.tests.observer.colorized_image_observer import ColorizedImageObserverTestCase
from colorization_program.tests.observer.pencil_config_observer import PencilConfigObserverTestCase
from colorization_program.tests.subject.colorization_process import ColorizationProcessSubjectTestCase
from colorization_program.tests.subject.pencil_config import PencilConfigSubjectTestCase
from colorization_program.tests.toolkit.image_processing_toolkit import ImageProcessingToolkitTestCase


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
