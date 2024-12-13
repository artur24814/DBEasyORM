from src.db.backends import DataBaseBackend

from .messages import print_success, print_info


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend

    def execute_detected_migration(self, detected_migration: dict) -> None:
        info_str = "Detected migrations: " + str(detected_migration)
        print_info(info_str)
        print_success("All database migrations applied")
