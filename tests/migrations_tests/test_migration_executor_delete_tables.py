import pytest
from faker import Faker
import random
from sqlite3 import OperationalError

from tests.models_tests.CustomeTestModel import (
    init_custome_test_model, init_post_test_model_related_to
)


fake = Faker()


def test_execute_query_tables_to_delete_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    from src.migrations import MigrationExecutor

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)
    # migarte this tables
    DETECTED_MIGRATIONS = {
        "create_tables": [CustomeTestModel, PostTestModel],
        "add_columns": [],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=DETECTED_MIGRATIONS)

    # test we actualy can access this models
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).save().execute() == 1

    DETECTED_DELETED_MIGRATIONS = {
        "create_tables": [],
        "add_columns": [],
        "drop_tables": [CustomeTestModel.query_creator.get_table_name(), PostTestModel.query_creator.get_table_name()],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=DETECTED_DELETED_MIGRATIONS)

    # Now we should have error
    with pytest.raises(OperationalError):
        assert CustomeTestModel(
            name=fake.name(),
            email=fake.email(),
            is_admin=random.choice([0, 1]),
            age=random.randint(15, 45),
            salary=round(random.uniform(5.000, 15.000), 3)
        ).save().execute() == 2

    with pytest.raises(OperationalError):
        PostTestModel.query_creator.all().execute()
