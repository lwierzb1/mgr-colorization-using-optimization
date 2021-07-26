__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.config.consts import HEX_BLACK, RGB_BLACK
from colorization_program.src.observer.observer import Observer


class PencilConfigObserver(Observer):
    def __init__(self):
        super().__init__()
        self.hex = HEX_BLACK
        self.bgr = RGB_BLACK
        self.width = 1

    def update_subject(self, **kwargs):
        width_value = kwargs.get('width')
        hex_value = kwargs.get('hex')
        bgr_value = kwargs.get('bgr')

        if width_value is not None:
            self.width = width_value

        if hex_value is not None:
            self.hex = hex_value

        if bgr_value is not None:
            self.bgr = bgr_value
