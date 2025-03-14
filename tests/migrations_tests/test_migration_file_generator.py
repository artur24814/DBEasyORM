import os
from dbeasyorm.migrations.services.migration_file_reader import MigrationFileReader
from dbeasyorm.migrations.services.migration_file_generator import MigrationFileGenerator
from dbeasyorm.migrations.domain.migration_model import MigrationModel
from dbeasyorm.migrations import CreateTableMigration
from tests.models_tests.CustomeTestModel import init_custome_test_model


def test_read_manual_migration():
    CustomeTestModel = init_custome_test_model()
    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend
    current_dir = os.path.dirname(os.path.abspath(__file__))
    migrations_generator = MigrationFileGenerator(app_dir=current_dir, db_backend=MigrationModel.query_creator.backend)
    detected_migration = [
        CreateTableMigration(
            table_name=CustomeTestModel.query_creator.get_table_name(),
            fields=CustomeTestModel._fields,
        )
    ]
    mig_hash = ''.join([migration.get_hash() for migration in detected_migration])
    migration_file_path = migrations_generator.create_migration_file(mig_hash, detected_migration)

    file_name = os.path.split(migration_file_path)[-1]
    assert "_".join(file_name.split('_')[1:]) == "create_table_CUSTOMETESTMODEL_.py"
    assert file_name.split('_')[0] == "012"

    reader = MigrationFileReader(app_dir=current_dir, db_backend=MigrationModel.query_creator.backend)
    migrations = reader.read_migrations()
    assert len(migrations) == 2

    assert isinstance(migrations[0], dict)
    assert len(migrations[1]["012"]) == 1
    for migration in migrations[1]["012"]:
        assert isinstance(migration, CreateTableMigration)
        assert migration.table_name == CustomeTestModel.query_creator.get_table_name()
        assert set(migration.fields.keys()) == set(CustomeTestModel._fields.keys())

    if os.path.exists(migration_file_path):
        os.remove(migration_file_path)
