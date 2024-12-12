import argparse

from .abstraction import BaseCommand
from src.migrations import Migration


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

    def handle(self, loockup_folder=None, id_migrations=None, restore=False, **kwargs) -> None:
        return Migration.update_database(
            loockup_folder=loockup_folder,
            id_migrations=id_migrations,
            restore=restore
        )
