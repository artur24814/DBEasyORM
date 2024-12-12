import argparse

from .abstraction import BaseCommand


class CommandManager:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CLI for My DBEasyORM")
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")
        self.commands = {}

    def register_command(self, command_class: BaseCommand) -> None:
        """
        Register a command by its class.
        :param command_class: A class inheriting from BaseCommand.
        """
        command = command_class()
        subparser = self.subparsers.add_parser(command.name(), help=command.help())
        command.configure_arguments(subparser)
        self.commands[command.name()] = command

    def run(self) -> None:
        """Parse arguments and execute the appropriate command."""
        args = self.parser.parse_args()

        if args.command in self.commands:
            # Pass parsed arguments as a dictionary to the command's handler
            command_args = vars(args)
            self.commands[args.command].handle(**command_args)
        else:
            self.parser.print_help()
