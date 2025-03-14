import os
from dbeasyorm.migrations.services.migration_file_reader import MigrationFileReader
from dbeasyorm.migrations.domain.migration_model import MigrationModel
from dbeasyorm.migrations.domain.migration import Migration
from tests.models_tests.CustomeTestModel import init_custome_test_model


def test_read_manual_migration():
    CustomeTestModel = init_custome_test_model()
    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reader = MigrationFileReader(app_dir=current_dir, db_backend=MigrationModel.query_creator.backend)
    migrations = reader.read_migrations()

    assert isinstance(migrations[0], dict)
    assert len(migrations[0]["001"]) == 3
    for migration in migrations[0]["001"]:
        assert issubclass(migration.__class__, Migration)
