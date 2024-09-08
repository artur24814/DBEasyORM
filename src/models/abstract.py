from abc import ABC, abstractmethod


class ModelABC(ABC):
    @abstractmethod
    def save(self) -> object:
        ...

    @abstractmethod
    def delete(self) -> int:
        ...
