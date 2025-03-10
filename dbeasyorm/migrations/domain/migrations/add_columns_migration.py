from dbeasyorm.db.backends import DataBaseBackend
from ..migration import Migration


class AddColumnsMigration(Migration):
    def __init__(self, table_name: str = None, fields: dict = None, db_columns: dict = None):
        super().__init__(table_name, fields)
        self.db_columns = db_columns

    def __repr__(self):
        fields_repr = ",\n        ".join(f"'{key}': {repr(value)}" for key, value in self.fields.items())
        db_columns_repr = ",\n        ".join(f"'{key}': {repr(value)}" for key, value in self.db_columns.items())

        return f"""{self.__class__.__name__}(
        table_name="{self.table_name}",
        fields={{\n        {fields_repr} \n    }},
        db_columns={{\n        {db_columns_repr} \n    }}
    )"""

    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        return backend.generate_alter_field_sql(
            table_name=self.table_name,
            fields=list(self.fields.values()),
            db_columns=self.db_columns
        )

    def get_hash(self) -> str:
        return f"add_columns_to_{self.table_name}_"
