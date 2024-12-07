import pytest
from src.DB_fields import fields


TEXT_FIELD = fields.TextField(field_name="email", null=True, unique=True, primary=True)


def test_Text_field_sql_line_creating():
    assert TEXT_FIELD.get_sql_line() == "email TEXT PRIMARY KEY"


def test_Text_field_is_valid():
    assert TEXT_FIELD.validate('sdfsdfdsfgds') is None


def test_Text_field_unsupported_types():
    with pytest.raises(TypeError):
        assert TEXT_FIELD.validate(12) is None
        assert TEXT_FIELD.validate(True) is None
        assert TEXT_FIELD.validate(12.23) is None
