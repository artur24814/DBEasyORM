from dbeasyorm.db.backends import DataBaseBackend
from dbeasyorm.models.model import Model


class MigrationDetecter:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend

    def get_detected_migrations(self, models: list) -> dict:
        db_schemas = self.get_database_schemas()
        return self.compare_schemas(models, db_schemas)

    def get_database_schemas(self) -> dict:
        self.db_backend.connect()
        return self.db_backend.get_database_schemas()

    def compare_schemas(self, models, db_schemas):
        migrations = {
            "create_tables": [],
            "drop_tables": [],
            "add_columns": [],
            "remove_columns": [],
        }

        for model in models:
            model_table_name = model.query_creator.get_table_name()
            if self.is_tables_exists_in_models_but_not_in_db(model_table_name, db_schemas.keys()):
                migrations["create_tables"].append(model)
                continue

            migrations = self.compare_cols_in_existing_tables(model_table_name, model, db_schemas, migrations)

        for table_name in db_schemas.keys():
            model_table_names = [model.query_creator.get_table_name() for model in models]
            if self.is_tables_exists_in_models_but_not_in_db(table_name, model_table_names):
                migrations["drop_tables"].append(table_name)

        return migrations

    def is_tables_exists_in_models_but_not_in_db(self, table_name: str, db_schemas_table_names: list) -> bool:
        return table_name not in db_schemas_table_names

    def compare_cols_in_existing_tables(self, table_name: str, model: Model, db_schemas: dict, migrations: dict) -> dict:
        db_columns = db_schemas[table_name]

        for field_name, field_instance in model._fields.items():
            if field_name not in db_columns:
                migrations["add_columns"].append((table_name, field_instance, model, db_columns))

        for column_name in db_columns.keys():
            if column_name not in list(model._fields.keys()):
                migrations["remove_columns"].append((table_name, column_name, model))

        return migrations

    def is_tables_exists_in_db_but_not_in_models(self, db_schemas_table_name: str, model_table_names: list) -> bool:
        return db_schemas_table_name not in model_table_names
