from .abstract import QueryCreatorABC
from src.DB_query.query_executor import QueryExecutor


class QueryCreator(QueryCreatorABC):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.sql = ''
        self.many = False
        self.values = ''

    def get_table_name(self):
        return self.get_class_name().__name__.upper()

    def get_class_name(self):
        if isinstance(self.model, type):
            return self.model
        return self.model.__class__

    def create(self, *args, **kwargs) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), values=self.values, fields=self.model._fields, return_id=True
        )

    def update(self, *args, **kwargs) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), values=self.values, fields=self.model._fields, return_id=True
        )

    def delete(self, id) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), values=self.values, fields=self.model._fields, return_id=True
        )

    def all(self) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), many=True
        )

    def get_one(self, *args, **kwargs) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), values=self.values, fields=self.model._fields
        )

    def filter(self, *args, **kwargs) -> QueryExecutor:
        return QueryExecutor(
            sql=self.sql, table_name=self.get_table_name(), values=self.values, fields=self.model._fields, many=True
        )
