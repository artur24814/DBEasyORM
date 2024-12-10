from .CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_featch_all_existing_instances_of_model(testing_db):
    CustomeTestModel = get_custome_test_model()
    assert CustomeTestModel.query_creator.all().execute() == []

    new_test_model1 = create_custome_test_model()
    new_test_model1.save().execute()

    new_test_model2 = create_custome_test_model()
    new_test_model2.save().execute()

    queryset = CustomeTestModel.query_creator.all().execute()

    assert len(queryset) == 2
    assert isinstance(queryset[0], CustomeTestModel) is True
    assert isinstance(queryset[1], CustomeTestModel) is True

    assert queryset[0].id != -1
    assert queryset[1].id != -1
