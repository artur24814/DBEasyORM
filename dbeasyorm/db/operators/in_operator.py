from .abstract import OperatorSQLABC
from .exeptions import UnsupportedOperatorValueTypes


class InSQLOperator(OperatorSQLABC):
    operator_name = "in"

    def apply(self, col=None, value=None, *args, **kwargs) -> str:
        if not isinstance(value, list):
            raise UnsupportedOperatorValueTypes(value=value, operator_name=self.operator_name)
        return f"{col} IN (" + ", ".join([f"'{inst}'" for inst in value]) + ")"
