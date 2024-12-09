def test_corrected_creating_delete_query(postgres_backend):
    assert postgres_backend.generate_delete_sql("USER", ('id',)) == \
        "DELETE FROM USER WHERE id = %s RETURNING *"

    assert postgres_backend.generate_delete_sql("USER", ('id', 'username')) == \
        "DELETE FROM USER WHERE id = %s AND username = %s RETURNING *"
