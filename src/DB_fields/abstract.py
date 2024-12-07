class BaseFieldMeta(type):
    def __new__(cls, name, bases, attrs):
        constraints = {}
        for attr_name, attr_value in attrs.items():
            if attr_name != "field_name":
                constraints[attr_name] = attr_value

        attrs['_constraints'] = constraints
        return super().__new__(cls, name, bases, attrs)


class BaseField(metaclass=BaseFieldMeta):
    def __init__(self, field_name=None, null=True, primary=False, unique=False):
        self.field_name = field_name
        self.null = null
        self.primary = primary
        self.unique = unique

    def __repr__(self):
        constrains_repr = ' '.join([f"{attr_name}={str(attr_value)}" for attr_name, attr_value in self._constraints])
        return f"<Field field_name={self.field_name} {constrains_repr}>"

    def get_sql_line(self) -> str:
        sql_line = self.get_basic_sql_line()
        if self.primary:
            sql_line += ' PRIMARY KEY'
        if not self.null and not self.primary:
            sql_line += ' NOT NULL'
        if self.unique and not self.primary:
            sql_line += ' UNIQUE'

        return sql_line

    def get_basic_sql_line(self) -> str:
        raise NotImplementedError()
