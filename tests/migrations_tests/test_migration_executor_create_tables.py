from faker import Faker
import random

from tests.models_tests.CustomeTestModel import (
    init_custome_test_model, init_post_test_model_related_to
)


fake = Faker()


def test_execute_query_one_table_to_create_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    from dbeasyorm.migrations import MigrationExecutor

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    DETECTED_MIGRATIONS = {
        "create_tables": [CustomeTestModel],
        "add_columns": [],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=DETECTED_MIGRATIONS)

    # now we can insert fist model
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).save().execute() == 1


def test_execute_query_few_relateds_to_create_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    from dbeasyorm.migrations import MigrationExecutor

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    DETECTED_MIGRATIONS = {
        "create_tables": [CustomeTestModel, PostTestModel],
        "add_columns": [],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=DETECTED_MIGRATIONS)

    # now we can insert fist models
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=random.choice([0, 1]),
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3)
    ).save().execute() == 1

    new_model = CustomeTestModel.query_creator.get_one(_id=1).execute()

    new_post_model = PostTestModel(is_read=False, autor=new_model, content=fake.text())
    assert new_post_model.save().execute() == 1
