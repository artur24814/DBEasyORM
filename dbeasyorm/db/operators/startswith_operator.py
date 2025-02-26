from .abstract import OperatorSQLABC


class StartsWithSQLOperator(OperatorSQLABC):
    operator_name = "startswith"

    def apply(self, col=None, value=None, *args, **kwargs) -> str:
        return f"{col} LIKE " + f"'{value}%'"
