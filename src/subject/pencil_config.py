from src.subject.subject import Subject


class PencilConfigSubject(Subject):
    def notify(self, **kwargs):
        for observer in self._observers:
            observer.update_subject(**kwargs)
