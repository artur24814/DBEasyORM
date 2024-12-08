from abc import ABC, abstractmethod


class DataBaseBackend(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def execute(self, query: str, params=None):
        ...
