from .abstract import QueryExecutorABC


class QueryExecutor(QueryExecutorABC):
    def __init__(self, sql, table_name=None, fields=None, values=None, many=False, return_id=False):
        self.cursor = None
        self.cnx = None
        self.sql = sql
        self.table_name = table_name
        self.fields = fields
        self.values = values
        self.many = many
        self.return_id = return_id

    def execute(self):
        pass
