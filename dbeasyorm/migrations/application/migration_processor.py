from colorama import Fore
from dbeasyorm.config import _get_active_backend

from ..services.migration_detecter import MigrationDetecter
from ..services.migration_executor import MigrationExecutor
from ..services.migration_file_reader import MigrationFileReader
from .cli.messages import print_success, print_line
from ..utils.model_classes_loader import ModelClassesLoader


class MigrationProcessor:
    def __init__(self, config_file_path: str = None):
        self.db_backend = _get_active_backend(config_file_path) if config_file_path else _get_active_backend()
        self.migration_detec = MigrationDetecter(self.db_backend)
        self.migration_file_reader = MigrationFileReader(db_backend=self.db_backend)
        self.migration_exec = MigrationExecutor(self.db_backend)
        self.models_loader = ModelClassesLoader()

    def update_database(self, loockup_folder: str, direct: bool, *args, **kwargs) -> None:
        print_line(Fore.GREEN, '=')
        models = self.models_loader.load_models(loockup_folder)
        detected_migration = self._get_migrations(models, direct)
        self.migration_exec.execute_detected_migration(detected_migration)
        print_success("Everything is up to date")
        print_line(Fore.GREEN, '=')

    def _get_migrations(self, models: list, direct: bool) -> list:
        return self.migration_detec.get_detected_migrations(models, formatted=True) \
            if direct else self.migration_file_reader.read_migrations()
