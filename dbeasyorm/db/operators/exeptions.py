class UnsupportedOperatorValueTypes(Exception):
    def __init__(self, value, code=None, operator_name=None):
        self.message = f"For the '{operator_name}' operator, the required value type is 'list', but the received type: {type(value)}"
        self.code = code

    def __str__(self):
        if self.code:
            return f"[Error {self.code}]: {self.message}"
        return self.message
