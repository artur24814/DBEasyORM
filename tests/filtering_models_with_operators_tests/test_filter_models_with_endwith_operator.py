from ..models_tests.CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_filtering_models_with_endswith_operator(testing_db):
    CustomeTestModel = get_custome_test_model()
    test_names = ["Jon", "Tom", "Jonathan", "James", "Bill"]

    for i in range(len(test_names)):
        new_test_model = create_custome_test_model(name=test_names[i])
        new_test_model.save().execute()

    assert CustomeTestModel.query_creator.filter(name__endswith="n").sql == \
        "SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE name LIKE '%n'"
    queryset_name = CustomeTestModel.query_creator.filter(name__endswith="n").execute()
    assert len(queryset_name) == 2
    assert test_names[0] in [obj.name for obj in queryset_name]
    assert test_names[2] in [obj.name for obj in queryset_name]
