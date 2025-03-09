from datetime import datetime
from dbeasyorm.migrations.domain.migration_model import Migration


class MigrationRepository:
    @staticmethod
    def get_model() -> Migration:
        return Migration

    @staticmethod
    def get_table_name() -> str:
        return Migration.query_creator.get_table_name()

    @staticmethod
    def ensure_migration_model() -> None:
        try:
            Migration.query_creator.all().execute()
        except Exception:
            MigrationRepository.init()
            print("Migrations table not found in database. New one created")

    @staticmethod
    def init() -> None:
        Migration.init_migration_model()

    @staticmethod
    def get_applied_migrations() -> list:
        return Migration.get_names_migrations_applied()

    @staticmethod
    def save_migration(name: str) -> None:
        Migration.query_creator.create(
            name=name,
            status=1,
            applied_at=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        ).execute()

    @staticmethod
    def get_next_name() -> str:
        return Migration.get_next_migration_name()
