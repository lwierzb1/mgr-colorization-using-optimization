from src.config.consts import HEX_BLACK, RGB_BLACK
from src.observer.observer import Observer


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
