from dbeasyorm.db.backends import DataBaseBackend
from ..migration import Migration


class DropTableMigration(Migration):
    def __repr__(self):
        return f'{self.__class__.__name__}(table_name="{self.table_name}")'

    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        return backend.generate_drop_table_sql(table_name=self.table_name)

    def get_hash(self) -> str:
        return f"drop_table_{self.table_name}_"
