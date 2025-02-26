from .abstract import OperatorSQLABC
from .exeptions import UnsupportedOperatorValueTypes


class BetweenSQLOperator(OperatorSQLABC):
    operator_name = "between"

    def apply(self, col=None, value=None, *args, **kwargs) -> str:
        if not isinstance(value, tuple):
            raise UnsupportedOperatorValueTypes(value=value, expected_type=tuple, operator_name=self.operator_name)
        return f"{col} BETWEEN {value[0]} AND {value[1]}"
