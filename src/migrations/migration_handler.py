from src.config import _get_active_backend

from .migration_detecter import MigrationDetecter
from .migration_executor import MigrationExecutor
from .messages import print_success, print_error
from .model_classes_loader import ModelClassesLoader


class MigrationHandler:
    def __init__(self):
        self.db_backend = _get_active_backend()
        self.migration_detec = MigrationDetecter(self.db_backend)
        self.migration_exec = MigrationExecutor(self.db_backend)
        self.models_loader = ModelClassesLoader()

    def update_database(self, loockup_folder: str, *args, **kwargs) -> None:
        models = self.models_loader.load_models(loockup_folder)
        detected_migration = self.migration_detec.get_detected_migrations(models)
        try:
            self.migration_exec.execute_detected_migration(detected_migration)
            print_success("Everything is up to date")
        except Exception as e:
            print_error(e)
