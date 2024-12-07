from .abstract import BaseField


class IntegerField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False, min=None, max=None):
        super().__init__(int, field_name, null, primary, unique)
        self.min = min
        self.max = max

    def get_basic_sql_line(self) -> str:
        return f'{self.field_name} INTEGER'

    def validate(self, value) -> None:
        super().validate(value)
        if self.min is not None and value < self.min:
            raise TypeError(f"Value for field '{self.field_name}' is less than {self.min}.")
        if self.max is not None and value > self.max:
            raise TypeError(f"Value for field '{self.field_name}' exceeds {self.max}.")


class TextField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(str, field_name, null, primary, unique)

    def get_basic_sql_line(self) -> str:
        return f'{self.field_name} TEXT'


class FloatField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(float, field_name, null, primary, unique)

    def get_basic_sql_line(self) -> str:
        return f'{self.field_name} REAL'


class ByteField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(bytes, field_name, null, primary, unique)

    def get_basic_sql_line(self) -> str:
        return f"{self.field_name} BLOB"

    def validate(self, value) -> None:
        super().validate(value)
        try:
            value.decode()
        except (UnicodeDecodeError, AttributeError):
            raise TypeError("The value is not the byte-like object")


class BooleanField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(int, field_name, null, primary, unique)

    def get_basic_sql_line(self) -> str:
        return f"{self.field_name} INTEGER"

    def validate(self, value) -> None:
        super().validate(value)
        if value not in (0, 1):
            raise TypeError(f"The value {value} cannot be converted to a logical value")
