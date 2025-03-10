import pytest
from faker import Faker

from dbeasyorm.migrations.domain.migration_model import MigrationModel
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository
from tests.models_tests.CustomeTestModel import init_custome_test_model


fake = Faker()


def test_init_migration(testing_db):
    CustomeTestModel = init_custome_test_model()
    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend

    # Balnc db
    with pytest.raises(Exception):
        assert len(MigrationModel.query_creator.all().execute()) == 0

    migration_repo = MigrationRepository(db_backend=MigrationModel.query_creator.backend)

    # create table and init model
    migration_repo.ensure_migration_model()
    migrations = MigrationModel.query_creator.all().execute()
    assert len(migrations) == 1
    assert migrations[0].name == '000'
    assert migrations[0].hash == 'create_table_MIGRATIONMODEL_'

    # add new one migration
    FAKE_MIG_NAME = "899"
    FAKE_MIG_HASH = "sdvfsdfdsdfg"

    migration_repo.save_migration(name=FAKE_MIG_NAME, hash=FAKE_MIG_HASH)

    migrations = MigrationModel.query_creator.all().execute()
    assert len(migrations) == 2
    assert migrations[1].name == FAKE_MIG_NAME
    assert migrations[1].hash == FAKE_MIG_HASH

    assert migration_repo.get_next_name() == "900"
