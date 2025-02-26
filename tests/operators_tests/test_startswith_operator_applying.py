from dbeasyorm.db.operators import apply_sql_operator


def test_correcting_startswith_operator():
    assert apply_sql_operator("name__startswith", "Jon") == "name LIKE 'Jon%'"
    assert apply_sql_operator("name__startswith", 1) == "name LIKE '1%'"
    assert apply_sql_operator("name__startswith", 1.00) == "name LIKE '1.0%'"
