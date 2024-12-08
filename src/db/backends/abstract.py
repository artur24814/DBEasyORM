from abc import ABC, abstractmethod


class DataBaseBackend(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        ...

    @abstractmethod
    def execute(self, query, params=None):
        ...
