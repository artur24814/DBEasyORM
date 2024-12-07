import pytest

from src.models.model import Model
from src.DB_fields import fields


@pytest.fixture
def custome_model():
    class CustomeModel(Model):
        id_user = fields.IntegerField(primary=True)
        name = fields.TextField(null=True)
        second_name = fields.TextField(null=True)
        age = fields.IntegerField(null=True)

    new_model = CustomeModel(name="Test", second_name="Test1", age=23)
    return new_model
