from dbeasyorm.db.backends import DataBaseBackend
from ..abstract import Migration


class AddColumnsMigration(Migration): 
    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        changes_sql = ", ".join([f"ADD COLUMN {change['name']} {change['type']}" for change in self.changes])
        return f"ALTER TABLE {self.table_name} {changes_sql};"
