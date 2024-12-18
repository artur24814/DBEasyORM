from .abstract import QueryCreatorABC
from dbeasyorm.config import _get_active_backend
from dbeasyorm.fields import ForeignKey
from dbeasyorm.models.exeptions import TheKeyIsNotAForeignKeyError
from .exeptions import TheInstanceDoesNotExistExeption
from .query_counter import QueryCounter
from .utils import insert_pattern_into_str


class QueryCreator(QueryCreatorABC):
    query_counter = QueryCounter()

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
        self.query_counter.register_query(self.sql)

        cursor = self.backend.execute(query=self.sql, params=self.values)
        return cursor.lastrowid if self.return_id else \
            (self._fetch_all(cursor) if self.many else self._fetch_one(cursor))

    def _fetch_one(self, cursor) -> object:
        data = cursor.fetchone()
        if not data:
            raise TheInstanceDoesNotExistExeption(instance_class=self.get_class_name())
        return self._map_row_to_object(data)

    def _fetch_all(self, cursor) -> list:
        rows = cursor.fetchall()
        return [self._map_row_to_object(row) for row in rows]

    def _map_row_to_object(self, row) -> object:
        column_names = [desc[0] for desc in self.backend.cursor.description]

        if not hasattr(self, "join_tables"):
            data = dict(zip(column_names, row))
            return self.model(**data)

        return self._map_row_to_object_with_relations(column_names, row)

    def _map_row_to_object_with_relations(self, column_names: list, row: list) -> object:
        base_model_data = {}
        related_model_data = {field: {} for field in self.join_tables.keys()}
        table_prefix_map = {data["table"]: field_name for field_name, data in self.join_tables.items()}

        for column, value in zip(column_names, row):
            table_prefix = next((prefix for prefix in table_prefix_map if column.startswith(prefix)), None)

            if table_prefix:
                related_field_name = table_prefix_map[table_prefix]
                field_name = column[len(table_prefix) + 1:]
                related_model_data[related_field_name][field_name] = value
            else:
                base_model_data[column] = value

        for related_field_name, data in self.join_tables.items():
            related_model_data[related_field_name] = data["model"](**related_model_data[related_field_name])

        base_model_data.update(related_model_data)
        delattr(self, 'join_tables')
        return self.model(**base_model_data)

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
        self.return_id = True
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

    def join(self, field_name: str, on: str = None, join_type: str = "INNER"):
        related_field_name = f"id_{field_name}"
        field_instance = self.model._fields.get(related_field_name)
        if not isinstance(field_instance, ForeignKey):
            raise TheKeyIsNotAForeignKeyError()

        join_table_name = field_instance.related_model.query_creator.get_table_name()

        if not hasattr(self, "join_tables"):
            self.join_tables = dict()
        self.join_tables[field_name] = {"table": join_table_name, "model": field_instance.related_model}

        alias_join_table_columns = ', '.join([f"{join_table_name}.{col} AS {join_table_name}_{col}" for col in field_instance.related_model._fields.keys()])

        self.sql = insert_pattern_into_str(r"(?i)(?=\bFROM\b)", f", {alias_join_table_columns} ", self.sql)
        self.sql += self.backend.generate_join_sql(
            join_table_name,
            on=f"{self.get_table_name()}.{related_field_name} = {join_table_name}._id" if not on else on,
            join_type=join_type
        )
        return self

    def get_one(self, *args, **kwargs) -> QueryCreatorABC:
        self.filter(*args, **kwargs)
        self.many = False
        return self

    def migrate_table(self, *args, **kwargs) -> QueryCreatorABC:
        self.sql = self.backend.generate_create_table_sql(
            table_name=self.get_table_name(),
            fields=list(kwargs.values())
        )
        return self
