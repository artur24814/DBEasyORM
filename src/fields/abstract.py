class BaseFieldMeta(type):
    def __new__(cls, name, bases, attrs):
        constraints = {}
        for attr_name, attr_value in attrs.items():
            if attr_name != "field_name":
                constraints[attr_name] = attr_value

        attrs['_constraints'] = constraints
        return super().__new__(cls, name, bases, attrs)


class BaseField(metaclass=BaseFieldMeta):
    def __init__(self, python_type, field_name=None, null=False, primary=False, unique=False, autoincrement=False):
        self.python_type = python_type
        self.field_name = field_name
        self.null = null
        self.primary = primary
        self.unique = unique
        self.autoincrement = autoincrement

    def __repr__(self):
        constrains_repr = ' '.join([f"{attr_name}={str(attr_value)}" for attr_name, attr_value in self._constraints])
        return f"<Field field_name={self.field_name} {constrains_repr}>"

    def get_sql_line(self) -> str:
        sql_line = self.get_basic_sql_line()
        if self.primary:
            sql_line += ' PRIMARY KEY'
        if self.autoincrement and self.primary:
            sql_line += ' AUTOINCREMENT'
        if self.null is False and not self.primary:
            sql_line += ' NOT NULL'
        if self.unique and not self.primary:
            sql_line += ' UNIQUE'

        return sql_line

    def get_basic_sql_line(self, sql_type: str) -> str:
        raise NotImplementedError("This method must be implemented in subclasses")

    def validate(self, value):
        if not isinstance(value, self.python_type):
            raise TypeError(
                f"Invalid value for field '{self.field_name}': "
                f"expected {self.python_type.__name__}, got {type(value).__name__}."
            )
