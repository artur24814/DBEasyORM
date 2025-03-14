from dbeasyorm.models.model import Model
from dbeasyorm import fields


class MigrationModel(Model):
    name = fields.TextField(unique=True)
    status = fields.IntegerField(default=0)
    applied_at = fields.TextField(null=True)
    hash = fields.TextField(null=True)

    @staticmethod
    def get_hash() -> str:
        return "create_table_MIGRATIONMODEL_"

    def init_migration_model(self) -> None:
        self.migrate().backend.execute(query=self.query_creator.sql)

    def get_next_migration_name(self) -> str:
        applied_migrations_name = self.get_names_migrations_applied()
        applied_migrations_name.sort()
        return str(int(applied_migrations_name[-1]) + 1).zfill(3)   # 001 format

    def get_names_migrations_applied(self) -> list:
        all_migrations = self.query_creator.filter(status=1).execute()
        return [migration.name for migration in all_migrations if migration.status == 1]
