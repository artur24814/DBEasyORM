from datetime import datetime
from dbeasyorm.migrations.domain.migration_model import MigrationModel


# class MigrationRepository:
#     def __init__(self, db_backend):
#         self.db_backend = db_backend
#         self.migration = Migration
#         self.migration.query_creator.backend = self.db_backend

#     def get_model(self) -> Migration:
#         return self.migration

#     def get_table_name(self) -> str:
#         return self.migration.query_creator.get_table_name()

#     def ensure_migration_model(self) -> None:
#         try:
#             self.migration.query_creator.all().execute()
#         except Exception:
#             self.init()
#             print("Migrations table not found in database. New one created")

#     def init(self) -> None:
#         self.migration.init_migration_model()

#     def get_applied_migrations(self) -> list:
#         return self.migration.get_names_migrations_applied()

#     def save_migration(self, name: str) -> None:
#         self.migration.query_creator.create(
#             name=name,
#             status=1,
#             applied_at=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#         ).execute()

#     def get_next_name(self) -> str:
#         return self.migration.get_next_migration_name()


class MigrationRepository:
    @staticmethod
    def get_model() -> MigrationModel:
        return MigrationModel

    @staticmethod
    def get_table_name() -> str:
        return MigrationModel.query_creator.get_table_name()

    @staticmethod
    def ensure_migration_model(db_backend) -> None:
        try:
            query = MigrationModel.query_creator.all()
            db_backend.execute(query.sql)
        except Exception:
            MigrationRepository.init(db_backend)
            print("Migrations table not found in database. New one created")

    @staticmethod
    def init(db_backend) -> None:
        MigrationModel.init_migration_model(db_backend)
        query = MigrationRepository.save_migration(name="000", hash=MigrationModel.get_hash())
        db_backend.execute(query=query.sql, params=query.values)

    @staticmethod
    def get_applied_migrations() -> list:
        return MigrationModel.get_names_migrations_applied()

    @staticmethod
    def save_migration(name: str, hash="") -> None:
        return MigrationModel.query_creator.create(
            name=name,
            status=1,
            applied_at=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            hash=hash
        )

    @staticmethod
    def get_next_name() -> str:
        return MigrationModel.get_next_migration_name()
