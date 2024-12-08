from .abstract import BaseField


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
