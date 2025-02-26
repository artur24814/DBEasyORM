from .abstract import OperatorSQLABC


class EndsWithSQLOperator(OperatorSQLABC):
    operator_name = "endswith"

    def apply(self, col=None, value=None, *args, **kwargs) -> str:
        return f"{col} LIKE " + f"'%{value}'"
