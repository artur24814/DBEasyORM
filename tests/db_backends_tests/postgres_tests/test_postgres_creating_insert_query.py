def test_corrected_creating_insert_query(postgres_backend):
    assert postgres_backend.generate_insert_sql("USER", ('name', 'email', 'age')) == \
        "INSERT INTO USER (name, email, age) VALUES (%s, %s, %s) RETURNING id"

    assert postgres_backend.generate_insert_sql("ADMIN", ('name', 'email', 'age', 'is_admin')) == \
        "INSERT INTO ADMIN (name, email, age, is_admin) VALUES (%s, %s, %s, %s) RETURNING id"
