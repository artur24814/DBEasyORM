from .abstract import QueryCreatorABC
from src.config import _get_active_backend


class QueryCreator(QueryCreatorABC):
    def __init__(self, model):
        super().__init__()
        self.backend = _get_active_backend()
        self.model = model
        self.sql = ''
        self.many = False
        self.values = ''
        self.cursor = None
        self.cnx = None
        self.values = None
        self.many = False
        self.return_id = False

    def execute(self) -> object:
        return self.backend.execute(query=self.sql, params=self.values)

    def get_table_name(self) -> str:
        return self.get_class_name().__name__.upper()

    def get_class_name(self) -> str:
        if isinstance(self.model, type):
            return self.model
        return self.model.__class__

    def create(self, *args, **kwargs) -> QueryCreatorABC:
        return self

    def update(self, *args, **kwargs) -> QueryCreatorABC:
        return self

    def delete(self, id) -> QueryCreatorABC:
        return self

    def all(self) -> QueryCreatorABC:
        return self

    def get_one(self, *args, **kwargs) -> QueryCreatorABC:
        return self

    def filter(self, *args, **kwargs) -> QueryCreatorABC:
        return self
