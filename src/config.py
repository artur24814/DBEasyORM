from .db.backends import SQLiteBackend, PostgreSQLBackend
import os


_active_backend = None

_registered_backends = {
    "sqlite": SQLiteBackend,
    "postgresql": PostgreSQLBackend
}


def register_backend(name, backend_class):
    if name in _registered_backends:
        raise ValueError(f"Backend '{name}' is already registered.")
    _registered_backends[name] = backend_class


def set_database_backend(backend_name, *args, **kwargs):
    global _active_backend

    if (backend := _registered_backends.get(backend_name)):
        _active_backend = backend(*args, **kwargs)
        _active_backend.connect(*args, **kwargs)
    else:
        raise ValueError(f"Unsupported backend: {backend_name}")


def _get_active_backend(config_file="dbeasyorm.ini"):
    if _active_backend is None:
        try:
            import configparser

            if config_file and os.path.exists(config_file):
                config_parser = configparser.ConfigParser()
                config_parser.read(config_file)
                if (db_config := dict(config_parser["database"])):
                    db_type = db_config.get("db_type")
                    if db_type is None:
                        raise ValueError("Database type ('db_type') is missing in the configuration.")

                    set_database_backend(db_type, **db_config)
                    return _active_backend
                raise RuntimeError(f"No database backend has been configured in {config_file}.")
        except ImportError:
            pass

        raise RuntimeError("No database backend has been configured.")
    return _active_backend


def _get_folders_for_migration_search(config_file="dbeasyorm.ini"):
    try:
        import configparser

        if config_file and os.path.exists(config_file):
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file)
            if (app_config := dict(config_parser["app"])):
                app_dir = app_config.get("dir")
                print('sdfasfas', app_dir)
                if app_dir is None:
                    raise ValueError(
                        "The specified folder for your application in which we will search for migrations is missing."
                        "Please set (dir) key = value"
                    )

                return app_dir
            raise RuntimeError(f"No application has been configured in {config_file}.")
    except ImportError:
        raise RuntimeError("Please install `configparser`")
