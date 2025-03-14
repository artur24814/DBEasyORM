from .abstract import BaseField
from .foreign_key import ForeignKey


def get_field_object_by_db_schema(column_definition: dict, field_mapping: dict = None, is_foreign_key: bool = False) -> BaseField:
    return generate_foreign_key_field_object(column_definition) if is_foreign_key else generate_field_object(column_definition, field_mapping)


def generate_field_object(column_definition: dict, field_mapping: dict) -> BaseField:
    return field_mapping[column_definition[2]](
        field_name=column_definition[1],
        null=bool(column_definition[3]),
        default=column_definition[4],
        primary=bool(column_definition[5])
    )


def generate_foreign_key_field_object(column_definition: dict) -> ForeignKey:
    return ForeignKey(
        related_model=column_definition[2],
        field_name=column_definition[3],
        on_delete=column_definition[6],
        null=True
    )
