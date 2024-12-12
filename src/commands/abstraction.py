from abc import ABC, abstractmethod
import argparse


class BaseCommand(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the command."""
        ...

    @abstractmethod
    def help(self) -> str:
        """Return the help description of the command."""
        ...

    @abstractmethod
    def configure_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure arguments for the command.
        :param parser: Argument parser for the command.
        """
        ...

    @abstractmethod
    def handle(self, **kwargs) -> None:
        """
        Handle the command logic.
        :param kwargs: Parsed arguments passed as keyword arguments.
        """
        ...
