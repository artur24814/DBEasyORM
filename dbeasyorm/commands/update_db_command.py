import argparse
import os

from dbeasyorm.migrations import MigrationHandler
from .abstraction import BaseCommand
from dbeasyorm.config import _get_folders_for_migration_search


class UpdateDatabaseCommand(BaseCommand):
    """Concrete implementation of the 'update-database' command."""

    def name(self) -> str:
        return "update-database"

    def help(self) -> str:
        return "Update the database."

    def configure_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-l", "--loockup-folder", type=str, help="Path to the lookup folder")
        parser.add_argument("-i", "--id-migrations", type=str, help="ID of specific migrations")
        parser.add_argument("-r", "--restore", action="store_true", help="Restore database to the previous state")
        parser.add_argument("-c", "--config", type=str, help="Path to the config.ini file")

    def handle(self, loockup_folder=None, id_migrations=None, restore=False, config_file=None, **kwargs) -> None:
        loockup_folder = os.path.join(os.getcwd(), _get_folders_for_migration_search()) if not loockup_folder else loockup_folder
        mig_handler = MigrationHandler(config_file)
        return mig_handler.update_database(
            loockup_folder=loockup_folder,
            id_migrations=id_migrations,
            restore=restore
        )
