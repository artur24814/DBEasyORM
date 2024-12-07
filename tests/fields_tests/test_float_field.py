import pytest
from src.DB_fields import fields


FLOAT_FIELD = fields.FloatField(field_name="price", unique=True)


def test_Float_field_sql_line_creating():
    assert FLOAT_FIELD.get_sql_line() == "price REAL NOT NULL UNIQUE"


def test_Float_field_is_valid():
    assert FLOAT_FIELD.validate(0.9) is None
    assert FLOAT_FIELD.validate(100.5) is None
    assert FLOAT_FIELD.validate(10.1) is None


def test_Float_field_unsupported_types():
    with pytest.raises(TypeError):
        assert FLOAT_FIELD.validate('asdsfadf') is None
        assert FLOAT_FIELD.validate(bool) is None
        assert FLOAT_FIELD.validate(23) is None
        assert FLOAT_FIELD.validate('23.0') is None
