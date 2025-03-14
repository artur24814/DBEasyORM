from colorama import Fore
from dbeasyorm.config import _get_active_backend

from ..services.migration_detecter import MigrationDetecter
from ..services.migration_executor import MigrationExecutor
from ..services.migration_file_reader import MigrationFileReader
from ..services.migration_rollbacker import MigrationRollbacker
from .cli.messages import print_success
from .cli.decorators import adding_separation_characters
from ..utils.model_classes_loader import ModelClassesLoader


class MigrationProcessor:
    def __init__(self, config_file_path: str = None):
        self.db_backend = _get_active_backend(config_file_path) if config_file_path else _get_active_backend()
        self.migration_detec = MigrationDetecter(self.db_backend)
        self.migration_file_reader = MigrationFileReader(db_backend=self.db_backend)
        self.migration_roll = MigrationRollbacker(db_backend=self.db_backend)
        self.migration_exec = MigrationExecutor(self.db_backend)
        self.models_loader = ModelClassesLoader()

    @adding_separation_characters(Fore.GREEN, print_message_fnc=lambda: print_success("Everything is up to date"))
    def update_database(self, loockup_folder: str, direct: bool, id_migrations: str, restore: bool, *args, **kwargs) -> None:
        models = self.models_loader.load_models(loockup_folder)
        detected_migration = self._get_migrations(models, direct, id_migrations)
        detected_migration.sort(key=lambda d: list(d.keys())[0])
        if restore:
            detected_migration = self.migration_roll.get_oposite_migrations(detected_migration)
        self.migration_exec.execute_detected_migration(detected_migration, restore=restore)

    def _get_migrations(self, models: list, direct: bool, id_migration: int) -> list:
        return self.migration_detec.get_detected_migrations(models, formatted=True) \
            if direct else self.migration_file_reader.read_migrations(id_migration=id_migration)
