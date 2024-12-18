from abc import ABC, abstractmethod


class QueryCreatorABC(ABC):

    @abstractmethod
    def execute(self) -> object:
        ...

    @abstractmethod
    def create(self, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def delete(self, *args) -> object:
        ...

    @abstractmethod
    def all(self) -> object:
        ...

    @abstractmethod
    def get_one(self, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def filter(self, *args, **kwargs) -> object:
        ...
