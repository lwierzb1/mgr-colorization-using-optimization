#!/usr/bin/env python3
import context
import unittest

from tests.observer.colorized_image_observer import ColorizedImageObserverTestCase
from tests.observer.pencil_config_observer import PencilConfigObserverTestCase
from tests.subject.colorization_process import ColorizationProcessSubjectTestCase
from tests.toolkit.image_processing_toolkit import ImageProcessingToolkitTestCase


def test_image_processing_toolkit():
    image_processing_toolkit_test_case = ImageProcessingToolkitTestCase()
    image_processing_toolkit_test_case.test_hex_to_bgr()


def test_colorized_image_observer():
    colorized_image_observer = ColorizedImageObserverTestCase()
    colorized_image_observer.test_update_subject()


def test_pencil_config_observer():
    pencil_config_observer = PencilConfigObserverTestCase()
    pencil_config_observer.test_update_subject()


def test_colorization_process_subject():
    colorization_process_subject = ColorizationProcessSubjectTestCase()
    colorization_process_subject.test_update()


if __name__ == '__main__':
    unittest.main()
