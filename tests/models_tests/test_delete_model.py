from .CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_delete_all_existing_instances_of_model(testing_db):
    CustomeTestModel = get_custome_test_model()

    new_test_model1 = create_custome_test_model()
    new_test_model1.save().execute()

    new_test_model2 = create_custome_test_model()
    new_test_model2.save().execute()

    queryset = CustomeTestModel.query_creator.all().execute()

    assert len(queryset) == 2

    for model in queryset:
        model.delete().execute()

    queryset_after_delete = CustomeTestModel.query_creator.all().execute()

    assert len(queryset_after_delete) == 0
