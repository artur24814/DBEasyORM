from abc import ABC, abstractmethod
from src.fields import BaseField


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
    def get_foreign_key_constraint(self, field_name, related_table, on_delete) -> str:
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
        ...

    @abstractmethod
    def generate_join_sql(self, table_name: str, on: str, join_type: str) -> str:
        ...

    @abstractmethod
    def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple) -> str:
        ...

    @abstractmethod
    def generate_delete_sql(self, table_name: str, where_clause: tuple) -> str:
        ...

    @abstractmethod
    def generate_create_table_sql(self, table_name: str, fields: BaseField) -> str:
        ...

    @abstractmethod
    def generate_alter_field_sql(self, *args, **kwargs) -> str:
        ...

    @abstractmethod
    def generate_drop_field_sql(self, *args, **kwargs) -> str:
        ...

    @abstractmethod
    def generate_drop_table_sql(self, table_name: str) -> str:
        ...

    @abstractmethod
    def get_database_schemas(self) -> dict:
        ...

    def get_sql_val_repr(self, value):
        return f"'{value}'" if isinstance(value, str) else ("NULL" if value is None else f"{value}")
