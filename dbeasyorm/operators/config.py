from .default import DefaultSQLOperator


_registered_operators = {
    "default": DefaultSQLOperator,
}


def register_operator(name, operator_class):
    if name in _registered_operators:
        raise ValueError(f"Operator '{name}' is already registered.")
    _registered_operators[name] = operator_class


def get_registered_operators():
    return _registered_operators
