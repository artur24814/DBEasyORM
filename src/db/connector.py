from src.config import _get_active_backend


class DatabaseConnector:
    def __int__(self):
        self.backend = _get_active_backend()

    def get_placeholder(self) -> str:
        return self.backend.get_placeholder()

    def connect(self, *args, **kwargs) -> object:
        return self.backend.connect(*args, **kwargs)

    def execute(self, *args, **kwargs) -> object:
        return self.backend.execute(*args, **kwargs)

    def generate_insert_sql(self, *args, **kwargs) -> str:
        return self.backend.generate_insert_sql(*args, **kwargs)

    def generate_update_sql(self, *args, **kwargs) -> str:
        return self.backend.generate_update_sql(*args, **kwargs)

    def generate_delete_sql(self, *args, **kwargs) -> str:
        return self.backend.generate_delete_sql(*args, **kwargs)
