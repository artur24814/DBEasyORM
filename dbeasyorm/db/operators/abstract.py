from abc import ABC, abstractmethod


class OperatorSQLABC(ABC):
    operator_name = None

    @abstractmethod
    def apply(self, col, value) -> str:
        ...

    def get_sql_val_repr(self, value: object) -> str:
        return f"'{value}'" if isinstance(value, str) else ("NULL" if value is None else f"{value}")
