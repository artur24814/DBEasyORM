def test_corrected_creating_insert_query(sqlite_backend):
    assert sqlite_backend.generate_insert_sql("USER", ('name', 'email', 'age')) == \
        "INSERT INTO USER (name, email, age) VALUES (?, ?, ?)"

    assert sqlite_backend.generate_insert_sql("ADMIN", ('name', 'email', 'age', 'is_admin')) == \
        "INSERT INTO ADMIN (name, email, age, is_admin) VALUES (?, ?, ?, ?)"
