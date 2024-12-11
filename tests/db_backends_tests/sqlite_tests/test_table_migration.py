from faker import Faker
import random

from tests.models_tests.CustomeTestModel import get_custome_test_model


fake = Faker()


def test_migration_query_sqlite(testing_db):
    CustomeTestModel = get_custome_test_model()

    CustomeTestModel.migrate()
    expected_sql = """CREATE TABLE IF NOT EXISTS CUSTOMETESTMODEL (_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, is_admin INTEGER, age INTEGER NOT NULL, salary REAL);"""

    normalized_actual = " ".join(CustomeTestModel.query_creator.sql.split())
    normalized_expected = " ".join(expected_sql.split())
    assert normalized_actual == normalized_expected


def test_using_model_after_migration_query(testing_db):
    CustomeTestModel = get_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    assert CustomeTestModel.query_creator.create(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).execute() == 1

    assert CustomeTestModel.query_creator.create(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).execute() == 2

    queryset = CustomeTestModel.query_creator.all().execute()

    assert len(queryset) == 2
    assert isinstance(queryset[0], CustomeTestModel) is True
    assert isinstance(queryset[1], CustomeTestModel) is True
