__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.subject.subject import Subject


class ColorizationProcessSubject(Subject):
    def notify(self, **kwargs):
        for observer in self._observers:
            observer.update_subject(**kwargs)
