import pytest
from dbeasyorm import fields


BOOLEAN_FIELD = fields.BooleanField(field_name="is_active", unique=True)


def test_Boolean_field_sql_line_creating():
    assert BOOLEAN_FIELD.get_sql_line() == "is_active INTEGER NOT NULL UNIQUE"


def test_Boolean_field_is_valid():
    assert BOOLEAN_FIELD.validate(0) is None
    assert BOOLEAN_FIELD.validate(1) is None
    assert BOOLEAN_FIELD.validate(True) is None


def test_Boolean_field_unsupported_types():
    with pytest.raises(TypeError):
        assert BOOLEAN_FIELD.validate(12) is None
        assert BOOLEAN_FIELD.validate("True") is None
