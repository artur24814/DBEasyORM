import argparse
import os

from dbeasyorm.migrations import MigrationFileManager
from .abstraction import BaseCommand
from dbeasyorm.config import _get_folders_for_migration_search


class GenerateMigrationCommand(BaseCommand):
    def name(self) -> str:
        return "generate-migration"

    def help(self) -> str:
        return "Generate migration file."

    def configure_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-l", "--loockup-folder", type=str, help="Path to the lookup folder")
        parser.add_argument("-c", "--config", type=str, help="Path to the config.ini file")

    def handle(self, loockup_folder=None, config_file=None, **kwargs) -> None:
        loockup_folder = os.path.join(os.getcwd(), _get_folders_for_migration_search()) if not loockup_folder else loockup_folder
        mig_handler = MigrationFileManager(config_file)
        return mig_handler.create_files(
            loockup_folder=loockup_folder,
        )
