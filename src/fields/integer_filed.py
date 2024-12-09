from .abstract import BaseField


class IntegerField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, autoincrement=False, unique=False, min=None, max=None):
        super().__init__(int, field_name, null, primary, unique, autoincrement)
        self.min = min
        self.max = max

    def get_basic_sql_line(self, sql_type="INTEGER") -> str:
        return f'{self.field_name} {sql_type}'

    def validate(self, value) -> None:
        super().validate(value)
        if self.min is not None and value < self.min:
            raise TypeError(f"Value for field '{self.field_name}' is less than {self.min}.")
        if self.max is not None and value > self.max:
            raise TypeError(f"Value for field '{self.field_name}' exceeds {self.max}.")
