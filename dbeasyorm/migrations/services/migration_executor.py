from colorama import Fore
from dbeasyorm.db.backends import DataBaseBackend

from ..cli.messages import print_success, print_info, print_line


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.sql = ""

    def execute_detected_migration(self, detected_migration: dict) -> None:
        print_line(Fore.BLUE, '-')
        print_info(f"Detected ({len(detected_migration)}) migrations to execute")
        print_line(Fore.BLUE, '-')

        self.sql = self._append_sql_migration(detected_migration, self.sql)

        self.db_backend.execute(query=self.sql)
        print_success("All database migrations applied")

    def _append_sql_migration(self, migrations: list, sql: str) -> str:
        for migration in migrations:
            sql += migration.generate_sql(self.db_backend)
        return sql
