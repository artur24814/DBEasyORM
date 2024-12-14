from colorama import Fore
from src.db.backends import DataBaseBackend, SQLiteBackend

from .messages import print_success, print_info, print_line


class MigrationExecutor:
    def __init__(self, db_backend: DataBaseBackend):
        self.db_backend = db_backend
        self.sql = ""

    def execute_detected_migration(self, detected_migration: dict) -> None:
        info_str = "Detected migrations: " + str(detected_migration)
        print_line(Fore.BLUE, '-')
        print_info(info_str)
        print_line(Fore.BLUE, '-')

        self.sql = self.append_table_creation_sql(detected_migration.get('create_tables'), self.sql)
        self.sql = self.append_delete_tables_sql(detected_migration.get('drop_tables'), self.sql)
        self.sql = self.append_insert_cols_sql(detected_migration.get('add_columns'), self.sql)
        self.sql = self.append_delete_cols_sql(detected_migration.get('remove_columns'), self.sql)

        self.db_backend.execute(query=self.sql)
        print_success("All database migrations applied")

    def append_table_creation_sql(self, models: list, sql: str) -> str:
        for model in models:
            model.migrate()
            sql += model.query_creator.sql
            sql += " \n"
        return sql

    def append_delete_tables_sql(self, columns: list, sql: str) -> str:
        for table_name in columns:
            sql += self.db_backend.generate_drop_table_sql(table_name=table_name)
        return sql

    def append_insert_cols_sql(self, columns: list, sql: str) -> str:
        if isinstance(self.db_backend, SQLiteBackend):
            unique_dict = {item[0]: (item[0], item[1], item[2], item[3]) for item in columns}
            unique_list = list(unique_dict.values())
            for _, _, model, db_columns in unique_list:
                sql += self.db_backend.generate_alter_field_sql(model=model, db_columns=db_columns)
        else:
            for table_name, col, _, _ in columns:
                sql += self.db_backend.generate_alter_field_sql(table_name=table_name, field=col)
        return sql

    def append_delete_cols_sql(self, columns: list, sql: str) -> str:
        if isinstance(self.db_backend, SQLiteBackend):
            unique_dict = {item[0]: (item[0], item[1], item[2]) for item in columns}
            unique_list = list(unique_dict.values())
            for _, _, model in unique_list:
                sql += self.db_backend.generate_drop_field_sql(model=model)
        else:
            for table_name, col, _, _ in columns:
                sql += self.db_backend.generate_drop_field_sql(table_name=table_name, field=col)
        return sql
