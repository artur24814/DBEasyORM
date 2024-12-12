from src.db.backends import DataBaseBackend


class MigrationDetecter:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend

    def get_database_schemas(self) -> dict:
        self.db_backend.connect()
        return self.db_backend.get_database_schemas()
