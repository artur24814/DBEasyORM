from src.DB_query.query_executor import QueryExecutor


class ModelABC:
    def save(self) -> QueryExecutor:
        ...

    def delete(self) -> QueryExecutor:
        ...
