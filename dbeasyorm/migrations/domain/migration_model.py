from dbeasyorm.models.model import Model
from dbeasyorm import fields


class MigrationModel(Model):
    name = fields.TextField()
    status = fields.IntegerField(default=0)
    applied_at = fields.TextField(null=True)
    hash = fields.TextField(null=True)

    @staticmethod
    def get_hash() -> str:
        return "create_table_MIGRATIONMODEL_"

    @staticmethod
    def init_migration_model(backend) -> None:
        backend.execute(MigrationModel.migrate().sql)

    @staticmethod
    def get_next_migration_name() -> str:
        applied_migrations_name = MigrationModel.get_names_migrations_applied()
        applied_migrations_name.sort()
        return str(int(applied_migrations_name[-1]) + 1).zfill(3)   # 001 format

    @staticmethod
    def get_names_migrations_applied() -> list:
        all_migrations = MigrationModel.query_creator.filter(status=1).execute()
        return [migration.name for migration in all_migrations if migration.status == 1]
