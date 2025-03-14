from datetime import datetime
from dbeasyorm.migrations.domain.migration_model import MigrationModel


class MigrationRepository:
    def __init__(self, db_backend):
        self.db_backend = db_backend
        self.model = MigrationModel()
        self.model.query_creator.backend = self.db_backend

    def get_model(self) -> MigrationModel:
        return self.model

    def get_table_name(self) -> str:
        return self.model.query_creator.get_table_name()

    def ensure_migration_model(self) -> None:
        if not self.migration_table_exists():
            self.init()
            print("Migrations table not found in database. New one created")

    def migration_table_exists(self) -> bool:
        try:
            self.model.query_creator.all().execute()
            return True
        except Exception:
            return False

    def init(self) -> None:
        self.model.init_migration_model()
        self.save_migration(name="000", hash=MigrationModel.get_hash())

    def save_migration(self, name: str, hash="") -> None:
        return self.model.query_creator.create(
            name=name,
            status=1,
            applied_at=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            hash=hash
        ).execute()

    def _fetch_migrations(self, filter_by: dict = None) -> list:
        query = self.model.query_creator
        if filter_by:
            query = query.filter(**filter_by)
        return query.execute()

    def get_applied_migrations(self) -> list:
        return self.model.get_names_migrations_applied()

    def get_migrations(self) -> list:
        return self._fetch_migrations()

    def get_migrations_in(self, in_list: list) -> list:
        return self._fetch_migrations({"name__in": in_list})

    def get_applied_migrations_obj(self) -> list:
        return self._fetch_migrations({"status": 1})

    def update_migration_status(self, name: str, status: int) -> MigrationModel:
        migration = self.model.query_creator.get_one(name=name).execute()
        migration.status = status
        migration.save().execute()
        return migration

    def update_migrations_status(self, status: int = 0, migrations_objs: list = None) -> list:
        result = []
        for migration in migrations_objs:
            migration.status = status
            migration.save().execute()
            result.append(migration)
        return result

    def get_next_name(self) -> str:
        return self.model.get_next_migration_name()
