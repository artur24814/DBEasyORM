from dbeasyorm.db.operators import apply_sql_operator


def test_correcting_endswith_operator():
    assert apply_sql_operator("name__endswith", "Jon") == "name LIKE '%Jon'"
    assert apply_sql_operator("name__endswith", 1) == "name LIKE '%1'"
    assert apply_sql_operator("name__endswith", 1.00) == "name LIKE '%1.0'"
