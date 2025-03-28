from colorama import Fore
from dbeasyorm.config import _get_active_backend

from ..services.migration_detecter import MigrationDetecter
from ..application.cli.messages import print_success
from ..utils.model_classes_loader import ModelClassesLoader
from ..services.migration_file_generator import MigrationFileGenerator
from .cli.decorators import adding_separation_characters


class MigrationFileManager:
    def __init__(self, config_file_path: str = None):
        self.db_backend = _get_active_backend(config_file_path) if config_file_path else _get_active_backend()
        self.migration_detec = MigrationDetecter(self.db_backend)
        self.migration_creator = MigrationFileGenerator(db_backend=self.db_backend)
        self.models_loader = ModelClassesLoader()

    @adding_separation_characters(Fore.GREEN)
    def create_files(self, loockup_folder: str, *args, **kwargs) -> None:
        models = self.models_loader.load_models(loockup_folder)
        detected_migration = self.migration_detec.get_detected_migrations(models)
        if any(detected_migration):
            mig_hash = ''.join([migration.get_hash() for migration in detected_migration])
            mig_path = self.migration_creator.create_migration_file(mig_hash, detected_migration)
            print_success(f"✅ New migration created: {mig_path}")
        else:
            print_success("Everything is up to date")
