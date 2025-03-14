from tests.models_tests.CustomeTestModel import init_custome_test_model, init_post_test_model_related_to
from dbeasyorm.migrations import AddColumnsMigration, DropTableMigration, RemoveColumnsMigration, CreateTableMigration


def test_one_table_to_create_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)

    from dbeasyorm.migrations.services.migration_detecter import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([PostTestModel, CustomeTestModel])

    assert len(detected_migrations) == 1
    assert detected_migrations[0].table_name == 'POSTTESTMODEL'
    assert isinstance(detected_migrations[0], CreateTableMigration)


def test_one_table_to_drop_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    PostTestModel.migrate().backend.execute(query=PostTestModel.query_creator.sql)

    from dbeasyorm.migrations.services.migration_detecter import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([CustomeTestModel])

    assert detected_migrations[0].table_name == 'POSTTESTMODEL'
    assert isinstance(detected_migrations[0], DropTableMigration)
    assert len(detected_migrations) == 1


def test_one_column_to_add_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    OldPostTestModel = init_post_test_model_related_to(CustomeTestModel)
    OldPostTestModel.migrate().backend.execute(query=OldPostTestModel.query_creator.sql)

    # add one moore column (title)
    from dbeasyorm.models.model import Model
    from dbeasyorm import fields

    class PostTestModel(Model):
        is_read = fields.BooleanField(null=True)
        autor = fields.ForeignKey(related_model=CustomeTestModel)
        content = fields.TextField(null=True)
        title = fields.TextField()

    from dbeasyorm.migrations.services.migration_detecter import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([PostTestModel, CustomeTestModel])

    assert len(detected_migrations) == 1
    assert isinstance(detected_migrations[0], AddColumnsMigration)
    assert detected_migrations[0].table_name == 'POSTTESTMODEL'
    assert len(detected_migrations[0].fields) == 5
    assert len(detected_migrations[0].db_columns) == 4


def test_one_column_to_delete_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    OldPostTestModel = init_post_test_model_related_to(CustomeTestModel)
    OldPostTestModel.migrate().backend.execute(query=OldPostTestModel.query_creator.sql)

    # delete column autor
    from dbeasyorm.models.model import Model
    from dbeasyorm import fields

    class PostTestModel(Model):
        is_read = fields.BooleanField(null=True)
        content = fields.TextField(null=True)

    from dbeasyorm.migrations.services.migration_detecter import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([CustomeTestModel, PostTestModel])

    assert len(detected_migrations) == 1
    assert isinstance(detected_migrations[0], RemoveColumnsMigration)
    assert detected_migrations[0].table_name == 'POSTTESTMODEL'
    assert len(detected_migrations[0].fields) == 3
    assert len(detected_migrations[0].db_columns) == 4
