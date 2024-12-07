import pytest
from src.DB_fields import fields


BITE_FIELD = fields.BiteField(field_name="image_bite", unique=True)


def test_BITE_FIELD_sql_line_creating():
    assert BITE_FIELD.get_sql_line() == "image_bite BLOB NOT NULL UNIQUE"


def test_BITE_FIELD_is_valid_value():
    assert BITE_FIELD.validate(b"hello") is None


def test_BITE_FIELD_unsupported_type_int():
    with pytest.raises(TypeError):
        assert BITE_FIELD.validate(12) is None


def test_BITE_FIELD_unsupported_type_str():
    with pytest.raises(TypeError):
        assert BITE_FIELD.validate("Hello") is None
