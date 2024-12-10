from .CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_filtering_models(testing_db):
    CustomeTestModel = get_custome_test_model()
    test_name = "Test"
    test_salary = 12.00

    for _ in range(10):
        new_test_model = create_custome_test_model(name=test_name)
        new_test_model.save().execute()

    for _ in range(15):
        new_test_model = create_custome_test_model(salary=test_salary)
        new_test_model.save().execute()

    queryset_name = CustomeTestModel.query_creator.filter(name=test_name).execute()
    assert len(queryset_name) == 10

    queryset_salary = CustomeTestModel.query_creator.filter(salary=test_salary).execute()
    assert len(queryset_salary) == 15
