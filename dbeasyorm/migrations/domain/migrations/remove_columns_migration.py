from dbeasyorm.db.backends import DataBaseBackend
from ..abstract import Migration


class RenoveColumnsMigration(Migration):
    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        return f"ALTER TABLE {self.table_name} DROP COLUMN {self.field_name};"
