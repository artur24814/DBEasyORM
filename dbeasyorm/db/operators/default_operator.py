from .abstract import OperatorSQLABC


class DefaultSQLOperator(OperatorSQLABC):
    operator_name = "default"

    def apply(self, col=None, value=None, *args, **kwargs) -> str:
        return f"{col} = " + self.get_sql_val_repr(value)
