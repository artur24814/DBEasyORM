from ..models_tests.CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_filtering_models_with_between_operator_using_int(testing_db):
    CustomeTestModel = get_custome_test_model()

    for i in range(10):
        new_test_model = create_custome_test_model(age=14 + i)
        new_test_model.save().execute()

    assert CustomeTestModel.query_creator.filter(age__between=(18, 60)).sql == \
        "SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE age BETWEEN 18 AND 60"
    queryset_age = CustomeTestModel.query_creator.filter(age__between=(18, 60)).execute()
    assert len(queryset_age) == 6


def test_filtering_models_with_between_operator_using_float(testing_db):
    CustomeTestModel = get_custome_test_model()

    for i in range(100):
        new_test_model = create_custome_test_model(salary=float(1000 + (10 * i)))
        new_test_model.save().execute()

    assert CustomeTestModel.query_creator.filter(salary__between=(1800.00, 2000.00)).sql == \
        "SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE salary BETWEEN 1800.0 AND 2000.0"
    queryset_salary = CustomeTestModel.query_creator.filter(salary__between=(1800.00, 2000.00)).execute()
    assert len(queryset_salary) == 20
