import subject


class ColorizationProcessSubject(subject.Subject):
    def notify(self, **kwargs):
        for observer in self._observers:
            observer.update_subject(**kwargs)
