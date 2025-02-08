import pytest
from dbeasyorm.db.operators import apply_sql_operator, UnsupportedOperatorValueTypes


def test_correcting_in_operator():
    assert apply_sql_operator("name__in", ["Jon", "Tom"]) == "name IN ('Jon', 'Tom')"


def test_using_in_operator_with_unsuported_value_type():
    with pytest.raises(UnsupportedOperatorValueTypes):
        assert apply_sql_operator("name__in", "Jon") is None
        assert apply_sql_operator("name__in", 1) is None
        assert apply_sql_operator("name__in", None) is None
