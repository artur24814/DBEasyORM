from colorama import Fore
from dbeasyorm.db.backends import DataBaseBackend
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository

from ..application.cli.messages import print_success, print_info, print_line


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.sql = ""

    def execute_detected_migration(self, detected_migration: dict) -> None:
        print_line(Fore.BLUE, '-')
        print_info(f"Detected ({len(detected_migration)}) migrations to execute")
        print_line(Fore.BLUE, '-')
        self._apply_migrations(detected_migration)
        print_success("All database migrations applied")

    def _apply_migrations(self, detected_migration: list):
        for migrations_dict in detected_migration:
            for name, migrations in migrations_dict.items():
                sql = self._append_sql_migration(migrations)
                self.db_backend.execute(query=sql)
                MigrationRepository.save_migration(name=name)
                print_success(f"✅ Migration {name} applied!")

    def _append_sql_migration(self, migrations: list) -> str:
        sql = ""
        for migration in migrations:
            sql += migration.generate_sql(self.db_backend)
        return sql
