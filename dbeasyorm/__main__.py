from dbeasyorm.commands import CommandManager, UpdateDatabaseCommand


def main():
    manager = CommandManager()

    # Register commands
    manager.register_command(UpdateDatabaseCommand)

    manager.run()


if __name__ == "__main__":
    main()
