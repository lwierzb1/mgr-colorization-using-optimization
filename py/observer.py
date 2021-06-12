import abc


class Observer(abc.ABC):
    @abc.abstractmethod
    def update_subject(self, **kwargs):
        pass
