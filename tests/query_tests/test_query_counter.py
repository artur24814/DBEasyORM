from tests.models_tests.CustomeTestModel import get_custome_test_model, create_custome_test_model
from dbeasyorm.query import QueryCreator


def test_query_counter_isolation(testing_db):
    CustomeTestModel = get_custome_test_model()

    with QueryCreator.query_counter:
        for _ in range(10):
            new_test_model = create_custome_test_model()
            new_test_model.save().execute()
        assert QueryCreator.query_counter.get_query_count() == 10

    with QueryCreator.query_counter:
        for _ in range(15):
            new_test_model = create_custome_test_model()
            new_test_model.save().execute()
        assert QueryCreator.query_counter.get_query_count() == 15

    with QueryCreator.query_counter:
        CustomeTestModel.query_creator.all().execute()
        assert QueryCreator.query_counter.get_query_count() == 1
