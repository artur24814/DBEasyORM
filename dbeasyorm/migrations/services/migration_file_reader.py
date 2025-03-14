import os
import importlib.util
from .migration_file_dir import MigrationFileDir
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository


class MigrationFileReader(MigrationFileDir):
    def __init__(self, config_file='dbeasyorm.ini', db_backend=None):
        super().__init__(config_file=config_file)
        self.db_backend = db_backend
        self.migration_repo = MigrationRepository(db_backend=self.db_backend)

    def read_migrations(self, id_migration: str = None) -> dict:
        migration_files = sorted(os.listdir(self.migrations_dir))
        applied_migrations_names = self.migration_repo.get_applied_migrations()

        if id_migration is not None:
            migration_files = [f for f in migration_files if f.split("_")[0] > id_migration]
            applied_migrations_names = []

        migrations_to_apply = list()

        for filename in migration_files:
            migration_name = filename.split("_")[0]
            migration_path = os.path.join(self.migrations_dir, filename)

            if not os.path.isfile(migration_path):
                continue

            if not filename.endswith(".py"):
                continue

            if migration_name not in applied_migrations_names:

                spec = importlib.util.spec_from_file_location("migration_module", migration_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "get_migrations"):
                    migrations = module.get_migrations()
                    migrations_to_apply.append({migration_name: migrations})

        return migrations_to_apply
