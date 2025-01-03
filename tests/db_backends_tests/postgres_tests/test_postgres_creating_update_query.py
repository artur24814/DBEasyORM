def test_corrected_creating_update_query(postgres_backend):
    assert postgres_backend.generate_update_sql("USER", ('name', 'age'), ('id',)) == \
        "UPDATE USER SET name = %s, age = %s WHERE id = %s RETURNING *"

    assert postgres_backend.generate_update_sql("USER", ('name', 'age'), ('id', 'is_admin')) == \
        "UPDATE USER SET name = %s, age = %s WHERE id = %s AND is_admin = %s RETURNING *"
