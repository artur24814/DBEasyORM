from dbeasyorm.db.backends import DataBaseBackend
from dbeasyorm.models.model import Model
from dbeasyorm.migrations.domain.migrations import (
    CreateTableMigration,
    DropTableMigration,
    AddColumnsMigration,
    RemoveColumnsMigration
)
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository


class MigrationDetecter:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.migration_repo = MigrationRepository(db_backend=self.db_backend)

    def get_detected_migrations(self, models: list, formatted=False) -> list:
        db_schemas = self._get_database_schemas()
        migrations = self._compare_schemas(models, db_schemas)
        return [] if not migrations else migrations if not formatted else [{self.migration_repo.get_next_name(): migrations}]

    def _get_database_schemas(self) -> dict:
        self.db_backend.connect()
        return self.db_backend.get_database_schemas()

    def _compare_schemas(self, models, db_schemas: dict) -> list:
        migrations = list()
        migrations = self._compare_models_to_db_schemas(models=models, db_schemas=db_schemas, migrations=migrations)
        migrations = self._compare_db_schema_to_models(models=models, db_schemas=db_schemas, migrations=migrations)
        return migrations

    def _compare_models_to_db_schemas(self, models: list, db_schemas: dict, migrations: list) -> list:
        for model in models:
            model_table_name = model.query_creator.get_table_name()
            if self._is_tables_exists_in_models_but_not_in_db(model_table_name, db_schemas.keys()):
                migration = CreateTableMigration(
                    table_name=model_table_name,
                    fields=model._fields,
                )
                migrations.append(migration)
                continue

            migrations = self._compare_cols_in_existing_tables(model_table_name, model, db_schemas, migrations)
        return migrations

    def _is_tables_exists_in_models_but_not_in_db(self, table_name: str, db_schemas_table_names: list) -> bool:
        return table_name not in db_schemas_table_names

    def _compare_cols_in_existing_tables(self, table_name: str, model: Model, db_schemas: dict, migrations: list) -> list:
        db_columns = db_schemas[table_name]

        for field_name in list(model._fields.keys()):
            if field_name not in db_columns:
                migration = AddColumnsMigration(
                    table_name=table_name,
                    fields=model._fields,
                    db_columns=db_columns,
                )
                migrations.append(migration)
                break

        for column_name in db_columns.keys():
            if column_name not in list(model._fields.keys()):
                migration = RemoveColumnsMigration(
                    table_name=table_name,
                    fields=model._fields,
                    db_columns=db_columns,
                )
                migrations.append(migration)
                break

        return migrations

    def _compare_db_schema_to_models(self, models, db_schemas: dict, migrations: list) -> list:
        model_table_names = {model.query_creator.get_table_name(): model for model in models}

        for table_name in db_schemas.keys():
            if self._is_tables_exists_in_db_but_not_in_models(table_name, list(model_table_names.keys())):
                if table_name != self.migration_repo.get_table_name():
                    migration = DropTableMigration(
                        table_name=table_name,
                        fields=db_schemas[table_name],
                    )
                    migrations.append(migration)
        return migrations

    def _is_tables_exists_in_db_but_not_in_models(self, db_schemas_table_name: str, model_table_names: list) -> bool:
        return db_schemas_table_name not in model_table_names
