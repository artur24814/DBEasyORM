from faker import Faker
import random

from dbeasyorm import fields

fake = Faker()


def init_custome_test_model():
    from dbeasyorm.models.model import Model

    class CustomeTestModel(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField()
        salary = fields.FloatField(null=True)

    return CustomeTestModel


def get_custome_test_model():
    model = init_custome_test_model()
    migrate_custome_test_model(model)
    return model


def init_post_test_model_related_to(related_model):
    from dbeasyorm.models.model import Model

    class PostTestModel(Model):
        is_read = fields.BooleanField(null=True)
        autor = fields.ForeignKey(related_model=related_model)
        content = fields.TextField(null=True)

    return PostTestModel


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


def create_custome_test_model(name=None, email=None, salary=None):
    CustomeTestModel = get_custome_test_model()
    return CustomeTestModel(
        name=name if name else fake.name(),
        email=email if email else fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=salary if salary else round(random.uniform(5.000, 15.000), 3)
    )
