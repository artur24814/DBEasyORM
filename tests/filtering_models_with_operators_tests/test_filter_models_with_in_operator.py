from ..models_tests.CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_filtering_models_with_in_perator(testing_db):
    CustomeTestModel = get_custome_test_model()
    test_names = [f"Test{i}" for i in range(10)]

    for i in range(10):
        new_test_model = create_custome_test_model(name=test_names[i])
        new_test_model.save().execute()

    assert CustomeTestModel.query_creator.filter(name__in=test_names[:3]).sql == \
        "SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE name IN ('Test0', 'Test1', 'Test2')"
    queryset_name = CustomeTestModel.query_creator.filter(name__in=test_names[:3]).execute()
    assert len(queryset_name) == 3
