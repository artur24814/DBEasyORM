import os
import datetime

from .migration_file_dir import MigrationFileDir
from .file_templates.migration_file_template import render_migration_file


class MigrationFileGenerator(MigrationFileDir):
    def __init__(self, config_file='dbeasyorm.ini'):
        super().__init__(config_file)
        self.migrations_dir = self.ensure_migrations_directory(os.path.join(self.app_dir, "migrations"))

    def ensure_migrations_directory(self, migrations_dir: str) -> None:
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
            print(f"Directory was created: {migrations_dir}")

        self.create_init_file_if_not_exists(migrations_dir)
        return migrations_dir

    def create_init_file_if_not_exists(self, migrations_dir: str) -> None:
        init_file = os.path.join(migrations_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("")

    def create_migration_file(self, name, migrations: dict):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{name}.py"
        filepath = os.path.join(self.migrations_dir, filename)

        def format_value(value):
            if isinstance(value, str):
                return f'"{value}"'
            elif isinstance(value, list):
                return "[" + ", ".join(format_value(v) for v in value) + "]"
            elif isinstance(value, dict):
                return "{\n        " + ",\n        ".join(f"{format_value(k)}: {format_value(v)}" for k, v in value.items()) + "\n    }"
            elif hasattr(value, '__repr__'):
                return repr(value)
            return str(value)

        formatted_mig = "{\n    " + ",\n    ".join(f"'{k}': {format_value(v)}" for k, v in migrations.items()) + "\n}"

        with open(filepath, "w") as f:
            f.write(render_migration_file(migration_name=name, migrations=formatted_mig))

        return filepath
