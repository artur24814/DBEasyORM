import pytest
import tempfile

from src import fields, set_database_backend

from src.db.backends import SQLiteBackend, PostgreSQLBackend


@pytest.fixture
def testing_db():
    _, db_path = tempfile.mkstemp()
    set_database_backend("sqlite", database_path=db_path)
    yield db_path


@pytest.fixture
def sqlite_backend(testing_db):
    return SQLiteBackend(database_path=testing_db)


@pytest.fixture
def postgres_backend():
    return PostgreSQLBackend(
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword"
    )


@pytest.fixture
def custome_model():
    from src.models.model import Model

    class CustomeModel(Model):
        name = fields.TextField(null=True)
        second_name = fields.TextField(null=True)
        age = fields.IntegerField(null=True)

    new_model = CustomeModel(name="Test", second_name="Test1", age=23)
    return new_model
