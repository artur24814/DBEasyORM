import pytest

from src.DB_query.query_executor import QueryExecutor
from src.models.exeptions import ThePrimaryKeyIsImmutable


def test_correcting_creating_fileds_when_models_init(custome_model):
    assert custome_model._fields is not None
    assert custome_model.age == 23
    assert custome_model.name == "Test"


def test_returning_executor_when_save_or_delete(custome_model):
    save_method = custome_model.save()
    delete_method = custome_model.delete()
    assert isinstance(save_method, QueryExecutor) is True
    assert isinstance(delete_method, QueryExecutor) is True


def test_throw_error_when_we_try_to_change_existing_id(custome_model):
    # set id
    custome_model.id = 12

    # change this id
    with pytest.raises(ThePrimaryKeyIsImmutable):
        custome_model.id = 123
