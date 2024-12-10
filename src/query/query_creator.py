from .abstract import QueryCreatorABC
from src.config import _get_active_backend


class QueryCreator(QueryCreatorABC):
    def __init__(self, model):
        super().__init__()
        self.backend = _get_active_backend()
        self.model = model
        self.cursor = None
        self.cnx = None
        self.setup_new_query_params()

    def setup_new_query_params(self):
        self.sql = ''
        self.many = False
        self.values = None
        self.return_id = False

    def execute(self) -> object:
        cursor = self.backend.execute(query=self.sql, params=self.values)
        return cursor.lastrowid if self.return_id else \
            (self._fetch_all(cursor) if self.many else self._fetch_one(cursor))

    def _fetch_one(self, cursor) -> object:
        data = cursor.fetchone()
        if not data:
            return None
        return self._map_row_to_object(data)

    def _fetch_all(self, cursor) -> list:
        rows = cursor.fetchall()
        return [self._map_row_to_object(row) for row in rows]

    def _map_row_to_object(self, row) -> object:
        column_names = [desc[0] for desc in self.backend.cursor.description]
        data = dict(zip(column_names, row))
        return self.model(**data)

    def get_table_name(self) -> str:
        return self.get_class_name().__name__.upper()

    def get_class_name(self) -> str:
        if isinstance(self.model, type):
            return self.model
        return self.model.__class__

    def create(self, *args, **kwargs) -> QueryCreatorABC:
        self.setup_new_query_params()
        self.sql = self.backend.generate_insert_sql(
            table_name=self.get_table_name(),
            columns=kwargs.keys()
        )
        self.return_id = True
        self.values = tuple(kwargs.values())
        return self

    def update(self, where: dict = None, *args, **kwargs) -> QueryCreatorABC:
        self.setup_new_query_params()
        self.sql = self.backend.generate_update_sql(
            table_name=self.get_table_name(),
            set_clause=tuple(kwargs.keys()),
            where_clause=tuple(where.keys())
        )
        self.return_id = True
        self.values = tuple(list(kwargs.values()) + list(where.values()))
        return self

    def delete(self, where: dict = None) -> QueryCreatorABC:
        self.setup_new_query_params()
        self.sql = self.backend.generate_delete_sql(
            table_name=self.get_table_name(),
            where_clause=tuple(where.keys())
        )
        self.values = tuple(where.values())
        return self

    def all(self, *args, **kwargs) -> QueryCreatorABC:
        return self.filter(*args)

    def filter(self, *args, **kwargs) -> QueryCreatorABC:
        self.setup_new_query_params()
        self.sql = self.backend.generate_select_sql(
            table_name=self.get_table_name(),
            columns=kwargs.get('columns', None),
            where_clause=kwargs
        )
        self.many = True
        return self

    def get_one(self, *args, **kwargs) -> QueryCreatorABC:
        self.setup_new_query_params()
        return self
