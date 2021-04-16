from abc import ABC, abstractmethod

from observer import Observer


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    @abstractmethod
    def notify(self, **kwargs):
        pass
