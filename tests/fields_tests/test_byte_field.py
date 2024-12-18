import pytest
from dbeasyorm import fields


BYTE_FIELD = fields.ByteField(field_name="image_bite", unique=True)


def test_Byte_field_sql_line_creating():
    assert BYTE_FIELD.get_sql_line() == "image_bite BLOB NOT NULL UNIQUE"


def test_Byte_field_is_valid_value():
    assert BYTE_FIELD.validate(b"hello") is None


def test_Byte_field_unsupported_types():
    with pytest.raises(TypeError):
        assert BYTE_FIELD.validate(12) is None
        assert BYTE_FIELD.validate("Hello") is None
        assert BYTE_FIELD.validate(12.3) is None
