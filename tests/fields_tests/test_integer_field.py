import pytest
from dbeasyorm import fields


INTEGER_FIELD = fields.IntegerField(field_name="age", null=True, unique=True, primary=True, min=0, max=10)


def test_Text_field_sql_line_creating():
    assert INTEGER_FIELD.get_sql_line() == "age INTEGER PRIMARY KEY"


def test_integer_field_is_valid():
    assert INTEGER_FIELD.validate(9) is None
    assert INTEGER_FIELD.validate(0) is None
    assert INTEGER_FIELD.validate(10) is None


def test_integer_field_unsupported_types():
    with pytest.raises(TypeError):
        assert INTEGER_FIELD.validate('asdsfadf') is None
        assert INTEGER_FIELD.validate(True) is None
        assert INTEGER_FIELD.validate(1.23) is None


def test_integer_field_out_of_range():
    with pytest.raises(TypeError):
        assert INTEGER_FIELD.validate(-1) is None
        assert INTEGER_FIELD.validate(23) is None
