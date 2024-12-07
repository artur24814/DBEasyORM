from .abstract import BaseField


class IntegerField(BaseField):
    def get_basic_sql_line(self) -> str:
        return f'{self.field_name} INTEGER'


class TextField(BaseField):
    def get_basic_sql_line(self):
        return f'{self.field_name} TEXT'


class RealField(BaseField):
    def get_basic_sql_line(self):
        return f'{self.field_name} REAL'


class BiteField(BaseField):
    def get_basic_sql_line(self):
        return f"{self.field_name} BLOB"
