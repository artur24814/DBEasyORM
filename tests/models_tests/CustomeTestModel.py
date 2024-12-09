from faker import Faker
import random

from src import fields

fake = Faker()


def get_custome_test_model():
    from src.models.model import Model

    class CustomeTestModel(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField()
        salary = fields.FloatField(null=True)

    model = CustomeTestModel
    migrate_custome_test_model(model)
    return model


def migrate_custome_test_model(custome_test_model):
    query_create_table = """
        CREATE TABLE IF NOT EXISTS CUSTOMETESTMODEL (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER,
        is_admin INTEGER,
        salary REAL
    );
    """
    custome_test_model.query_creator.backend.connect()
    custome_test_model.query_creator.backend.execute(query=query_create_table)


def create_custome_test_model():
    CustomeTestModel = get_custome_test_model()
    return CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    )