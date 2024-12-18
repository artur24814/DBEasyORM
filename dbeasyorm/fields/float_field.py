from .abstract import BaseField


class FloatField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False, default=None):
        super().__init__(float, field_name, null, primary, unique, default=None)

    def get_basic_sql_line(self, sql_type="REAL") -> str:
        return f'{self.field_name} {sql_type}'
