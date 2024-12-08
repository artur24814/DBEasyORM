from abc import ABC, abstractmethod


class DataBaseBackend(ABC):
    @abstractmethod
    def get_placeholder(self) -> str:
        ...

    @abstractmethod
    def get_sql_type(self, type: type) -> str:
        ...

    @abstractmethod
    def get_sql_types_map(self) -> dict:
        ...

    @abstractmethod
    def connect(self, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def execute(self, query: str, params=None):
        ...

    def generate_insert_sql(self, table_name: str, columns: tuple) -> str:
        ...

    @abstractmethod
    def generate_select_sql(self, table_name: str, columns: tuple, where_clause: tuple, limit: int = None, offset: int = None) -> str:
        pass

    @abstractmethod
    def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple) -> str:
        ...

    @abstractmethod
    def generate_delete_sql(self, table_name: str, where_clause: tuple) -> str:
        ...
