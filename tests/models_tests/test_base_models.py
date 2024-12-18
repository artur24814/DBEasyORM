import pytest

from dbeasyorm.query import QueryCreator
from dbeasyorm.models.exeptions import ThePrimaryKeyIsImmutable


def test_correcting_creating_fileds_when_models_init(testing_db, custome_model):
    assert custome_model._fields is not None
    assert custome_model.age == 23
    assert custome_model.name == "Test"


def test_returning_query_creator_when_save_or_delete(testing_db, custome_model):
    save_method = custome_model.save()
    delete_method = custome_model.delete()
    assert isinstance(save_method, QueryCreator) is True
    assert isinstance(delete_method, QueryCreator) is True


def test_throw_error_when_we_try_to_change_existing_id(testing_db, custome_model):
    # set id
    custome_model.id = 12

    # change this id
    with pytest.raises(ThePrimaryKeyIsImmutable):
        custome_model.id = 123


def test_throw_error_when_we_try_to_change_field_to_unsupported_type(testing_db, custome_model):
    custome_model.age = "12"

    with pytest.raises(TypeError):
        custome_model.save()
