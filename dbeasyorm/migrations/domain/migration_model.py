import datetime
from dbeasyorm.models.model import Model
from dbeasyorm import fields


class Migration(Model):
    name = fields.TextField()
    status = fields.IntegerField(default=0)
    applied_at = fields.TextField(null=True)
    hash = fields.TextField(null=True)

    @staticmethod
    def init_migration_model() -> None:
        Migration.migrate().backend.execute(query=Migration.query_creator.sql)
        Migration.query_creator.create(
            name="000",
            status=1,
            applied_at=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ).execute()

    @staticmethod
    def get_next_migration_name() -> str:
        applied_migrations_name = Migration.get_names_migrations_applied()
        applied_migrations_name.sort()
        return str(int(applied_migrations_name[-1]) + 1).zfill(3)   # 001 format

    @staticmethod
    def get_names_migrations_applied() -> list:
        all_migrations = Migration.query_creator.filter(status=1).execute()
        return [migration.name for migration in all_migrations if migration.status == 1]
