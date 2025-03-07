import os
from .migration_file_dir import MigrationFileDir


class MigrationFileReader(MigrationFileDir):

    def read_migrations(self) -> dict:
        migration_files = sorted(os.listdir(self.migrations_dir))

        for filename in migration_files:
            # migration_id = filename.split("_")[0]
            migration_path = os.path.join(self.migrations_dir, filename)

            migration_globals = {}
            with open(migration_path) as f:
                exec(f.read(), migration_globals)

            if "get_migrations" in list(migration_globals.keys()):
                migrations = migration_globals["get_migrations"]()
                return migrations
        return list()
