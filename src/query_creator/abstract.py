from abc import ABC, abstractmethod
from src.DB_query.query_executor import QueryExecutor


class QueryCreatorABC(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> QueryExecutor:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> QueryExecutor:
        ...

    @abstractmethod
    def all(self) -> QueryExecutor:
        ...

    @abstractmethod
    def get_one(self, *args, **kwargs) -> QueryExecutor:
        ...

    @abstractmethod
    def filter(self, *args, **kwargs) -> QueryExecutor:
        ...
