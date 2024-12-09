from .CustomeTestModel import get_custome_test_model, create_custome_test_model


def test_update_existin_model(testing_db):
    CustomeTestModel = get_custome_test_model()
    new_test_model1 = create_custome_test_model()
    new_test_model1.save().execute()

    created_model = CustomeTestModel.query_creator.all().execute()[0]
    
    assert created_model.name != 'Brand New Name'
    created_model.name = 'Brand New Name'
    created_model.save().execute()

    updated_model = CustomeTestModel.query_creator.all().execute()[0]
    
    assert updated_model.name == 'Brand New Name'
