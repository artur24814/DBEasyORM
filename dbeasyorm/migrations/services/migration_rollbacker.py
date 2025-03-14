from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository


class MigrationRollbacker:
    def __init__(self, db_backend=None):
        self.db_backend = db_backend
        self.migration_repo = MigrationRepository(db_backend=self.db_backend)

    def rollback_migrations(self, migration_names: list) -> list:
        migration_objs = self.migration_repo.get_migrations_in(migration_names)
        updated_migrations = self.migration_repo.update_migrations_status(status=0, migrations_objs=migration_objs)

        return sorted(updated_migrations, key=lambda mig: int(mig.name))

    def get_oposite_migrations(self, migrations: list) -> list:
        migration_names = list()
        oposite_migs = list()

        for migration_dict in migrations:
            migration_names.append(*list(migration_dict.keys()))
            for mig_name, values in migration_dict.items():
                oposite_migs.append({mig_name: [migration.get_opposite_migration() for migration in values]})

        self.rollback_migrations(migration_names=migration_names)
        return sorted(oposite_migs, key=lambda d: list(d.keys())[0], reverse=True)
