from dbeasyorm.db.backends import DataBaseBackend
from ..migration import Migration


class CreateTableMigration(Migration):

    def generate_sql(self, backend: DataBaseBackend, *args, **kwargs) -> str:
        sql = backend.generate_create_table_sql(
            table_name=self.table_name,
            fields=list(self.fields.values())
        )
        return sql + " \n"

    def get_hash(self) -> str:
        return f"create_table_{self.table_name}_"

    def get_opposite_migration(self) -> Migration:
        from ..migrations import DropTableMigration
        return DropTableMigration(
            table_name=self.table_name,
            fields=self.fields
        )
