from colorama import Fore
from dbeasyorm.db.backends import DataBaseBackend
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository

from ..application.cli.messages import print_success, print_info
from ..application.cli.decorators import adding_separation_characters


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.migration_repo = MigrationRepository(db_backend=self.db_backend)
        self.migration_repo.ensure_migration_model()
        self.sql = ""

    @adding_separation_characters(Fore.BLUE, character='-', print_message_fnc=lambda: print_success("All database migrations applied"))
    def execute_detected_migration(self, detected_migration: dict, restore: bool = False) -> None:
        print_info(f"Detected ({len(detected_migration)}) migrations to execute")
        self._apply_migrations(detected_migration, restore)

    def _apply_migrations(self, detected_migration: list, restore: bool) -> None:
        for migrations_dict in detected_migration:
            for name, migrations in migrations_dict.items():
                sql = self._append_sql_migration(migrations)
                migration_hash = self._append_migration_hash(migrations)
                self._apply_one_migration(sql=sql, name=name, migration_hash=migration_hash, restore=restore)

    def _append_sql_migration(self, migrations: list) -> str:
        return ''.join([migration.generate_sql(self.db_backend) for migration in migrations])

    def _append_migration_hash(self, migrations: list) -> str:
        return ''.join([migration.get_hash() for migration in migrations])

    def _apply_one_migration(self, name: str, sql: str, migration_hash: str, restore: bool) -> None:
        self.db_backend.execute(query=sql)
        if not restore:
            try:
                self.migration_repo.save_migration(name=name, hash=migration_hash)
            except Exception:
                self.migration_repo.update_migration_status(name=name, status=1)
            print_success(f"✅ Migration {name} applied!")
        else:
            print_success(f"✅ Migration {name} rollback!")
