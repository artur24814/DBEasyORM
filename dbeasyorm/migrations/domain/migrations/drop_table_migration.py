from dbeasyorm.db.backends import DataBaseBackend
from ..migration import Migration


class DropTableMigration(Migration):

    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        return backend.generate_drop_table_sql(table_name=self.table_name)

    def get_hash(self) -> str:
        return f"drop_table_{self.table_name}_"

    def get_opposite_migration(self) -> Migration:
        from ..migrations import CreateTableMigration
        return CreateTableMigration(
            table_name=self.table_name,
            fields=self.fields
        )
