from .default_operator import DefaultSQLOperator
from .in_operator import InSQLOperator
from .startswith_operator import StartsWithSQLOperator
from .endswith_operator import EndsWithSQLOperator
from .between_operator import BetweenSQLOperator


_registered_operators = {
    DefaultSQLOperator.operator_name: DefaultSQLOperator,
    InSQLOperator.operator_name: InSQLOperator,
    StartsWithSQLOperator.operator_name: StartsWithSQLOperator,
    EndsWithSQLOperator.operator_name: EndsWithSQLOperator,
    BetweenSQLOperator.operator_name: BetweenSQLOperator,
}


def register_operator(name, operator_class):
    if name in _registered_operators:
        raise ValueError(f"Operator '{name}' is already registered.")
    _registered_operators[name] = operator_class


def get_registered_operators():
    return _registered_operators
