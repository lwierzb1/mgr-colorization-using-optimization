__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.observer.observer import Observer


class ColorizedImageObserver(Observer):
    def __init__(self):
        self.x_start = None
        self.y_start = None
        self.result = None

    def update_subject(self, **kwargs):
        self.x_start = kwargs.get('x_start')
        self.y_start = kwargs.get('y_start')
        self.result = kwargs.get('result')
