def test_corrected_creating_delete_query(sqlite_backend):
    assert sqlite_backend.generate_delete_sql("USER", ('id',)) == \
        "DELETE FROM USER WHERE id=?"

    assert sqlite_backend.generate_delete_sql("USER", ('id', 'username')) == \
        "DELETE FROM USER WHERE id=? AND username=?"
