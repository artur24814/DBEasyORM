import pytest
from faker import Faker

from dbeasyorm.migrations.domain.migration_model import MigrationModel
from tests.models_tests.CustomeTestModel import init_custome_test_model
from dbeasyorm.migrations import CreateTableMigration
from dbeasyorm.migrations.services.migration_executor import MigrationExecutor


fake = Faker()


def test_execute_first_few_migration(testing_db):
    CustomeTestModel = init_custome_test_model()

    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend
    with pytest.raises(Exception):
        assert len(MigrationModel.query_creator.all().execute()) == 0

    migration_exec = MigrationExecutor(db_backend=MigrationModel.query_creator.backend)
    migrations = MigrationModel.query_creator.all().execute()
    assert len(migrations) == 1
    assert migrations[0].name == '000'
    assert migrations[0].hash == 'create_table_MIGRATIONMODEL_'

    detected_migration = [
        {
            "001":
            [
                CreateTableMigration(
                    table_name=CustomeTestModel.query_creator.get_table_name(),
                    fields=CustomeTestModel._fields,
                )
            ]
        }
    ]

    migration_exec.execute_detected_migration(detected_migration=detected_migration)

    migrations = MigrationModel.query_creator.all().execute()
    assert len(migrations) == 2
    assert migrations[1].name == '001'
    assert migrations[1].hash == 'create_table_CUSTOMETESTMODEL_'
