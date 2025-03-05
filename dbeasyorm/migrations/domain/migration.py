from abc import ABC, abstractmethod
from dbeasyorm.db.backends import DataBaseBackend


class Migration(ABC):
    def __init__(self, table_name: str = None, fields: dict = None):
        self.table_name = table_name
        self.fields = fields

    def __repr__(self):
        fields_repr = ",\n        ".join(f"'{key}': {repr(value)}" for key, value in self.fields.items())

        return f"""{self.__class__.__name__}(
        table_name="{self.table_name}",
        fields={{\n        {fields_repr} \n    }}
    )"""

    @abstractmethod
    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        pass
