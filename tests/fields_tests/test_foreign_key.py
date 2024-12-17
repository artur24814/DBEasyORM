import pytest
from src import fields
from tests.models_tests.CustomeTestModel import get_custome_test_model


def get_foreign_key():
    CustomeTestModel = get_custome_test_model()
    return fields.ForeignKey(related_model=CustomeTestModel)


def test_foreign_key_sql_line_creating_for_sqlite(sqlite_backend):
    FOREIGN_KEY = get_foreign_key()
    FOREIGN_KEY.field_name = "user_id"
    assert FOREIGN_KEY.get_sql_line(
        db_backend_constrain_gen=sqlite_backend.get_foreign_key_constraint
    ) == ('user_id INTEGER ', 'FOREIGN KEY (user_id) REFERENCES CUSTOMETESTMODEL (_id) ON DELETE CASCADE')


def test_foreign_key_sql_line_creating_for_postgres(postgres_backend):
    FOREIGN_KEY = get_foreign_key()
    FOREIGN_KEY.field_name = "user_id"
    assert FOREIGN_KEY.get_sql_line(
        db_backend_constrain_gen=postgres_backend.get_foreign_key_constraint
    ) == "user_id INTEGER, CONSTRAINT fk_user_id_to_CUSTOMETESTMODEL FOREIGN KEY (user_id) REFERENCES CUSTOMETESTMODEL (_id) ON DELETE CASCADE"


def test_integer_field_is_valid():
    FOREIGN_KEY = get_foreign_key()
    assert FOREIGN_KEY.validate(9) is None
    assert FOREIGN_KEY.validate(0) is None
    assert FOREIGN_KEY.validate(10) is None


def test_integer_field_unsupported_types():
    FOREIGN_KEY = get_foreign_key()
    with pytest.raises(TypeError):
        assert FOREIGN_KEY.validate('asdsfadf') is None
        assert FOREIGN_KEY.validate(True) is None
        assert FOREIGN_KEY.validate(1.23) is None
