import pytest

from .CustomeTestModel import get_custome_test_model, create_custome_test_model
from dbeasyorm.query import TheInstanceDoesNotExistExeption


def test_get_one_model(testing_db):
    CustomeTestModel = get_custome_test_model()
    test_name = "Test"
    test_salary = 12.00

    for _ in range(10):
        new_test_model = create_custome_test_model(name=test_name)
        new_test_model.save().execute()

    for _ in range(15):
        new_test_model = create_custome_test_model(salary=test_salary)
        new_test_model.save().execute()

    queryset_name = CustomeTestModel.query_creator.get_one(name=test_name).execute()
    assert isinstance(queryset_name, CustomeTestModel) is True

    queryset_salary = CustomeTestModel.query_creator.get_one(salary=test_salary).execute()
    assert isinstance(queryset_salary, CustomeTestModel) is True

    with pytest.raises(TheInstanceDoesNotExistExeption):
        CustomeTestModel.query_creator.get_one(name="Testssdjagd").execute()
