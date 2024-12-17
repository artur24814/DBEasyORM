def test_corrected_generation_join_query(sqlite_backend):
    assert sqlite_backend.generate_join_sql(
        "USER",
        on="POST.id_user = USER._id",
        join_type="INNER"
    ) == " INNER JOIN USER ON POST.id_user = USER._id"
