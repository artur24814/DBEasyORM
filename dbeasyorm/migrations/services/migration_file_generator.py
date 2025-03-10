import subprocess

from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository

from ..utils.file_handling import create_file_if_not_exists, create_file
from .migration_file_dir import MigrationFileDir
from .file_templates.migration_file_template import render_migration_file
from .file_templates.init_migration_file_template import render_init_migration_file


class MigrationFileGenerator(MigrationFileDir):
    def __init__(self, config_file='dbeasyorm.ini', db_backend=None):
        super().__init__(config_file)
        self.db_backend = db_backend
        self._ensure_migration_model_in_db()
        self._ensure_first_migration_file_exists(self.migrations_dir)

    def _ensure_migration_model_in_db(self) -> None:
        MigrationRepository.ensure_migration_model(self.db_backend)

    def _ensure_first_migration_file_exists(self, migration_dir: str) -> None:
        init_migration_script = render_init_migration_file(MigrationRepository.get_model())
        filepath = create_file_if_not_exists(migration_dir, "000_init_migration.py", init_migration_script)
        self._apply_formatting_into_file(filepath)

    def create_migration_file(self, name, migrations: dict) -> str:
        filepath = create_file(
            dir=self.migrations_dir,
            file_name=self._get_file_name(name, migrations),
            content=render_migration_file(migration_name=name, migrations=migrations)
        )
        self._apply_formatting_into_file(filepath)

        return filepath

    def _get_file_name(self, name: str, migrations: list) -> str:
        next_name = MigrationRepository.get_next_name()
        filename = f"{next_name}_{name}.py"
        return filename

    def _apply_formatting_into_file(self, filepath: str) -> None:
        subprocess.run(["black", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
