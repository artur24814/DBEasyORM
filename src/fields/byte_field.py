from .abstract import BaseField


class ByteField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False):
        super().__init__(bytes, field_name, null, primary, unique)

    def get_basic_sql_line(self, sql_type="BLOB") -> str:
        return f"{self.field_name} {sql_type}"

    def validate(self, value) -> None:
        super().validate(value)
        try:
            value.decode()
        except (UnicodeDecodeError, AttributeError):
            raise TypeError(
                 f"Invalid value for field '{self.field_name}': "
                 f"The {value} is not the byte-like object")
