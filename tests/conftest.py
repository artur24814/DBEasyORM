import pytest

from src.models.model import Model
from src.DB_fields import base_field


@pytest.fixture
def custome_model():
    class CustomeModel(Model):
        name = base_field.BaseField(field_type="blabla", null=True, primary=True)
        second_name = base_field.BaseField(field_type="blabla", null=True)
        age = base_field.BaseField(field_type="int", null=True)

    new_model = CustomeModel(name="Test", second_name="Test1", age=23)
    return new_model
