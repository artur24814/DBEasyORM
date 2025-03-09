import os
import configparser


class MigrationFileDir:
    def __init__(self, config_file='dbeasyorm.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.app_dir = self.get_app_directory(self.config, self.config_file)
        self.migrations_dir = self._ensure_migrations_directory(os.path.join(self.app_dir, "migrations"))

    def get_app_directory(self, config: configparser.ConfigParser, config_file: str) -> str:
        config.read(config_file)
        if "app" in config and "dir" in config["app"]:
            return config["app"]["dir"]
        else:
            raise ValueError("⚠️ [app] section not found in configuration file!")

    def _ensure_migrations_directory(self, migrations_dir: str) -> str:
        from ..utils.file_handling import create_directory_if_not_exists, create_file_if_not_exists
        migrations_dir = create_directory_if_not_exists(migrations_dir)
        create_file_if_not_exists(migrations_dir, "__init__.py", "")
        return migrations_dir
