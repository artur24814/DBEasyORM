import pytest
from dbeasyorm.db.operators import apply_sql_operator, UnsupportedOperatorValueTypes


def test_correcting_between_operator():
    assert apply_sql_operator("age__between", (18, 60)) == "age BETWEEN 18 AND 60"


def test_error_index_between_operator():
    with pytest.raises(IndexError):
        assert apply_sql_operator("age__between", (18,)) is None


def test_using_between_operator_with_unsuported_value_type():
    with pytest.raises(UnsupportedOperatorValueTypes):
        assert apply_sql_operator("age__between", "Jon") is None
        assert apply_sql_operator("age__between", 1) is None
        assert apply_sql_operator("age__between", None) is None
