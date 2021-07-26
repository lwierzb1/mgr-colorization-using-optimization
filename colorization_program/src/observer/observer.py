__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import abc


class Observer(abc.ABC):
    @abc.abstractmethod
    def update_subject(self, **kwargs):
        pass
