from dbeasyorm.commands import CommandManager, ApplyMigrationsCommand, GenerateMigrationCommand


def main():
    manager = CommandManager()

    # Register commands
    manager.register_command(ApplyMigrationsCommand)
    manager.register_command(GenerateMigrationCommand)

    manager.run()


if __name__ == "__main__":
    main()
