from faker import Faker
import random

from tests.models_tests.CustomeTestModel import (
    init_custome_test_model, init_post_test_model_related_to
)
from dbeasyorm.migrations import CreateTableMigration


fake = Faker()


def test_execute_query_one_table_to_create_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    from dbeasyorm.migrations.services.migration_executor import MigrationExecutor

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)
    detected_migration = [
        {
            "011":
            [
                CreateTableMigration(
                    table_name=CustomeTestModel.query_creator.get_table_name(),
                    fields=CustomeTestModel._fields,
                )
            ]
        }
    ]
    migration_exec.execute_detected_migration(detected_migration=detected_migration)

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
    from dbeasyorm.migrations.services.migration_executor import MigrationExecutor

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    detected_migration = [
        {
            "011":
            [
                CreateTableMigration(
                    table_name=CustomeTestModel.query_creator.get_table_name(),
                    fields=CustomeTestModel._fields,
                ),
                CreateTableMigration(
                    table_name=PostTestModel.query_creator.get_table_name(),
                    fields=PostTestModel._fields,
                )
            ]
        }
    ]

    migration_exec.execute_detected_migration(detected_migration=detected_migration)

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
