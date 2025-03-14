import pytest
from faker import Faker
import random

from tests.models_tests.CustomeTestModel import init_custome_test_model
from dbeasyorm.migrations import RemoveColumnsMigration


fake = Faker()


def test_execute_few_columns_to_add_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    from dbeasyorm.migrations.services.migration_executor import MigrationExecutor
    from dbeasyorm import fields
    from dbeasyorm.models.model import Model

    # 1. Delete this fields from model
    class CustomeTestModel(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        # is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField()
        salary = fields.FloatField(null=True)

    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)

    db_schemas = migration_exec.db_backend.get_database_schemas()
    detected_migration = [{
        "011":
            [
                RemoveColumnsMigration(
                    table_name=CustomeTestModel.query_creator.get_table_name(),
                    fields=CustomeTestModel._fields,
                    db_columns=db_schemas[CustomeTestModel.query_creator.get_table_name()],
                )
            ]
        }
    ]
    migration_exec.execute_detected_migration(detected_migration=detected_migration)

    # now we can insert model and try to get deleted fileds
    assert CustomeTestModel(
        name=fake.name(),
        email=fake.email(),
        is_admin=1,
        age=random.randint(15, 45),
        salary=round(random.uniform(5.000, 15.000), 3),
    ).save().execute() == 1

    created_model = CustomeTestModel.query_creator.get_one(_id=1).execute()

    # try to get this field
    with pytest.raises(AttributeError):
        assert created_model.is_admin == 1
