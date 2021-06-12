import subject


class ColorizedImageSubject(subject.Subject):
    def notify(self, **kwargs):
        for observer in self._observers:
            observer.update_subject(**kwargs)
