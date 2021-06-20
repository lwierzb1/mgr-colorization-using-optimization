import tests.context
from unittest import TestCase, main

from src.toolkit.image_processing import hex_to_bgr


class ImageProcessingToolkitTestCase(TestCase):
    def test_hex_to_bgr(self):
        self._test_hex_to_bgr_black()
        self._test_hex_to_bgr_white()
        self._test_hex_to_bgr_red()

    def _test_hex_to_bgr_black(self):
        hex_value = '#000000'
        black = [0, 0, 0]
        self.assertEqual(black, hex_to_bgr(hex_value))

    def _test_hex_to_bgr_white(self):
        hex_value = '#ffffff'
        white = [255, 255, 255]
        self.assertEqual(white, hex_to_bgr(hex_value))

    def _test_hex_to_bgr_red(self):
        hex_value = '#ff0000'
        red = [0, 0, 255]
        self.assertEqual(red, hex_to_bgr(hex_value))


if __name__ == '__main__':
    main()
