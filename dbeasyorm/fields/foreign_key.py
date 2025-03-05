from .abstract import BaseField


class ForeignKey(BaseField):
    def __init__(self, related_model, field_name=None, null=True, primary=False, autoincrement=False, unique=False, on_delete="CASCADE", default=None):
        super().__init__(int, field_name, null, primary, unique, autoincrement, default)
        self.related_model = related_model
        self.on_delete = on_delete

    def get_sql_line(self, db_backend_constrain_gen=None) -> str:
        related_model_name = self.related_model if isinstance(self.related_model, str) else self.related_model.__name__.upper()
        return db_backend_constrain_gen(self.field_name, related_model_name, self.on_delete)

    def get_basic_sql_line(self, sql_type="INTEGER") -> str:
        return f'{self.field_name} {sql_type}'

    def validate(self, value):
        super().validate(value)
        if not isinstance(value, int):
            raise TypeError(
                f"Invalid value for ForeignKey field '{self.field_name}': expected int, got {type(value).__name__}."
            )
