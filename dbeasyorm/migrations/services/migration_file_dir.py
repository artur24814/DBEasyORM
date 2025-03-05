from abc import ABC
import os
import configparser


class MigrationFileDir(ABC):
    def __init__(self, config_file='dbeasyorm.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.app_dir = self.get_app_directory(self.config, self.config_file)
        self.migrations_dir = os.path.join(self.app_dir, "migrations")

    def get_app_directory(self, config: configparser.ConfigParser, config_file: str) -> str:
        config.read(config_file)

        if "app" in config and "dir" in config["app"]:
            return config["app"]["dir"]
        else:
            raise ValueError("⚠️ [app] section not found in configuration file!")
