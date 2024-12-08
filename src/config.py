from .db.backends import SQLiteBackend


_active_backend = None

_registered_backends = {
    "sqlite": SQLiteBackend
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


def _get_active_backend():
    if _active_backend is None:
        raise RuntimeError("No database backend has been configured.")
    return _active_backend
