from .abstract import BaseField


class BooleanField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False, default=None):
        super().__init__(int, field_name, null, primary, unique, default)

    def get_basic_sql_line(self, sql_type="INTEGER") -> str:
        return f"{self.field_name} {sql_type}"

    def validate(self, value) -> None:
        super().validate(value)
        if value not in (0, 1):
            raise TypeError(
                f"Invalid value for field '{self.field_name}': "
                f"The value {value} cannot be converted to a logical value"
            )
