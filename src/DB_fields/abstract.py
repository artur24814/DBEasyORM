from abc import ABC, abstractmethod


class FieldABC(ABC):
    @abstractmethod
    def get_sql(self):
        ...
