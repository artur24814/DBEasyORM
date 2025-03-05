from colorama import Fore
from dbeasyorm.db.backends import DataBaseBackend

from ..cli.messages import print_success, print_info, print_line


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.sql = ""

    def execute_detected_migration(self, detected_migration: dict) -> None:
        info_str = "Detected migrations: " + str(detected_migration)
        print_line(Fore.BLUE, '-')
        print_info(info_str)
        print_line(Fore.BLUE, '-')

        for migration_list in detected_migration.values():
            self.sql = self.append_sql_migration(migration_list, self.sql)

        self.db_backend.execute(query=self.sql)
        print_success("All database migrations applied")

    def append_sql_migration(self, migrations: list, sql: str) -> str:
        for migration in migrations:
            sql += migration.generate_sql(self.db_backend)
        return sql
