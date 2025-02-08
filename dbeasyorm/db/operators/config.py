from .default_operator import DefaultSQLOperator
from .in_operator import InSQLOperator


_registered_operators = {
    DefaultSQLOperator.operator_name: DefaultSQLOperator,
    InSQLOperator.operator_name: InSQLOperator
}


def register_operator(name, operator_class):
    if name in _registered_operators:
        raise ValueError(f"Operator '{name}' is already registered.")
    _registered_operators[name] = operator_class


def get_registered_operators():
    return _registered_operators
