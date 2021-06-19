from src.subject.subject import Subject


class PencilConfigSubject(Subject):
    def __init__(self):
        super().__init__()

    def notify(self, **kwargs):
        for observer in self._observers:
            observer.update_subject(**kwargs)
