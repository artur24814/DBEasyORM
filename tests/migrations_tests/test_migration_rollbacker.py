from faker import Faker

from dbeasyorm.migrations.domain.migration_model import MigrationModel
from dbeasyorm.migrations import CreateTableMigration, AddColumnsMigration, RemoveColumnsMigration, DropTableMigration
from dbeasyorm.migrations.services.migration_rollbacker import MigrationRollbacker
from dbeasyorm.migrations.infrastructure.migration_repository import MigrationRepository
from tests.models_tests.CustomeTestModel import init_custome_test_model, init_post_test_model_related_to


fake = Faker()


def test_rollback_migration_return_correct_type_response(testing_db):
    CustomeTestModel = init_custome_test_model()
    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend
    migration_repo = MigrationRepository(db_backend=MigrationModel.query_creator.backend)

    # create table and init model
    migration_repo.ensure_migration_model()

    for i in range(1, 51):
        migration_repo.save_migration(name=str(i).zfill(3), hash=fake.text())

    migrations = MigrationModel.query_creator.all().execute()
    assert len(migrations) == 51

    mig_rollbacker = MigrationRollbacker(db_backend=MigrationModel.query_creator.backend)

    result_migration = mig_rollbacker.rollback_migrations(migration_names=['046', '047', '048', '049', '050'])
    assert isinstance(result_migration, list)
    assert len(result_migration) == 5

    for migration in result_migration:
        assert issubclass(migration.__class__, MigrationModel)


def test_rollback_migration_change_migration_status_in_db(testing_db):
    CustomeTestModel = init_custome_test_model()
    MigrationModel.query_creator.backend = CustomeTestModel.query_creator.backend
    migration_repo = MigrationRepository(db_backend=MigrationModel.query_creator.backend)

    # create table and init model
    migration_repo.ensure_migration_model()

    for i in range(1, 51):
        migration_repo.save_migration(name=str(i).zfill(3), hash=fake.text())

    assert len(MigrationModel.query_creator.all().execute()) == 51

    mig_rollbacker = MigrationRollbacker(db_backend=MigrationModel.query_creator.backend)

    result_migration = mig_rollbacker.rollback_migrations(migration_names=['046', '047', '048', '049', '050'])
    assert len(result_migration) == 5

    for migration in result_migration:
        assert migration.status == 0

    assert len(migration_repo.get_applied_migrations_obj()) == 46


def test_get_oposite_migrations(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.query_creator.backend.connect()
    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    from dbeasyorm.migrations.services.migration_executor import MigrationExecutor
    migration_exec = MigrationExecutor(db_backend=CustomeTestModel.query_creator.backend)
    migration_repo = MigrationRepository(db_backend=MigrationModel.query_creator.backend)

    # create table and init model
    migration_repo.ensure_migration_model()

    for i in range(1, 13):
        migration_repo.save_migration(name=str(i).zfill(3), hash=fake.text())

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

    mig_rollbacker = MigrationRollbacker(db_backend=MigrationModel.query_creator.backend)

    oposite_migrations = mig_rollbacker.get_oposite_migrations(detected_migration)
    assert len(oposite_migrations[0]["011"]) == 2
    assert isinstance(oposite_migrations[0]["011"][0], DropTableMigration)
    assert isinstance(oposite_migrations[0]["011"][1], DropTableMigration)

    migration_exec.execute_detected_migration(detected_migration=detected_migration)
    db_schemas = migration_exec.db_backend.get_database_schemas()

    new_detected_migration = [
        {
            "012":
            [
                RemoveColumnsMigration(
                    table_name=CustomeTestModel.query_creator.get_table_name(),
                    fields=CustomeTestModel._fields,
                    db_columns=db_schemas[CustomeTestModel.query_creator.get_table_name()],
                ),
                AddColumnsMigration(
                    table_name=PostTestModel.query_creator.get_table_name(),
                    fields=PostTestModel._fields,
                    db_columns=db_schemas[PostTestModel.query_creator.get_table_name()],
                )
            ]
        }
    ]

    new_oposite_migrations = mig_rollbacker.get_oposite_migrations(new_detected_migration)
    assert len(new_oposite_migrations[0]["012"]) == 2
    assert isinstance(new_oposite_migrations[0]["012"][0], AddColumnsMigration)
    assert new_oposite_migrations[0]["012"][0].table_name == CustomeTestModel.query_creator.get_table_name()
    assert new_oposite_migrations[0]["012"][0].fields == db_schemas[CustomeTestModel.query_creator.get_table_name()]
    assert new_oposite_migrations[0]["012"][0].db_columns == CustomeTestModel._fields
    assert isinstance(new_oposite_migrations[0]["012"][1], RemoveColumnsMigration)
    assert new_oposite_migrations[0]["012"][1].table_name == PostTestModel.query_creator.get_table_name()
    assert new_oposite_migrations[0]["012"][1].fields == db_schemas[PostTestModel.query_creator.get_table_name()]
    assert new_oposite_migrations[0]["012"][1].db_columns == PostTestModel._fields
