from abc import ABC, abstractmethod


class QueryExecutorABC(ABC):
    @abstractmethod
    def execute(self):
        ...
