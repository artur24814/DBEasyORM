from .abstract import BaseField


class FloatField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(float, field_name, null, primary, unique)

    def get_basic_sql_line(self, sql_line="REAL") -> str:
        return f'{self.field_name} {sql_line}'
