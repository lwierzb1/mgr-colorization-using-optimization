from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update_subject(self, **kwargs):
        pass
