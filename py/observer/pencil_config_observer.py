from py.config.consts import HEX_BLACK, RGB_BLACK
from py.observer.observer import Observer


class PencilConfigObserver(Observer):
    def __init__(self):
        super().__init__()
        self.hex = HEX_BLACK
        self.rgb = RGB_BLACK
        self.width = 1

    def update_subject(self, **kwargs):
        width_value = kwargs.get('width')
        hex_value = kwargs.get('hex')
        rgb_value = kwargs.get('rgb')

        if width_value is not None:
            self.width = width_value

        if hex_value is not None:
            self.hex = hex_value

        if rgb_value is not None:
            self.rgb = rgb_value
