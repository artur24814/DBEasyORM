from dbeasyorm.db.operators import apply_sql_operator


def test_correcting_default_operator():
    assert apply_sql_operator("name", "Jon") == "name = 'Jon'"


def test_using_default_operator_with_nonsens_query():
    assert apply_sql_operator("name__sacfasf", "Jon") == "name = 'Jon'"
