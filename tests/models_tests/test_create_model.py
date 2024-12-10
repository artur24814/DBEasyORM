from .CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_creating_new_models_by_using_save(testing_db):
    new_test_model1 = create_custome_test_model()

    new_test_model1.save()
    assert new_test_model1.id == -1
    assert new_test_model1.query_creator.return_id is True

    returned_value = new_test_model1.query_creator.execute()
    assert returned_value == 1

    new_test_model2 = create_custome_test_model()
    assert new_test_model2.save().execute() == 2


def test_creating_new_models_by_create(testing_db):
    CustomeTestModel = get_custome_test_model()
    assert CustomeTestModel.query_creator.create(
        name="Jon",
        email="Jon@example.com",
        is_admin=1,
        age=34,
        salary=13.000
    ).execute() == 1
