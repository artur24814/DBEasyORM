from .abstract import BaseField


def get_field_object_by_schema(db_schema: dict, fields: dict = None, fk: bool = False) -> BaseField:
    field = generate_field_object(db_schema, fields) if not fk else generate_foreign_key_field_object(db_schema)
    return field


def generate_field_object(db_schema, fields):
    args = dict(
        field_name=db_schema[1],
        null=bool(db_schema[3]),
        default=db_schema[4],
        primary=bool(db_schema[5])
    )
    return fields[db_schema[2]](**args)


def generate_foreign_key_field_object(db_schema):
    from .foreign_key import ForeignKey
    args = dict(
        related_model=db_schema[2],
        field_name=db_schema[3],
        on_delete=db_schema[6],
        null=True
    )
    return ForeignKey(**args)
