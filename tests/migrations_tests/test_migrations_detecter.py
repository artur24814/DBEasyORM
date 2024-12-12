from tests.models_tests.CustomeTestModel import init_custome_test_model, init_post_test_model_related_to


def test_one_table_to_create_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)

    from src.migrations import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([PostTestModel, CustomeTestModel])

    assert detected_migrations.get('create_tables') == ['POSTTESTMODEL']
    assert detected_migrations.get('drop_tables') == []
    assert detected_migrations.get('add_columns') == []
    assert detected_migrations.get('remove_columns') == []


def test_one_table_to_drop_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    PostTestModel = init_post_test_model_related_to(CustomeTestModel)
    PostTestModel.migrate().backend.execute(query=PostTestModel.query_creator.sql)

    from src.migrations import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([CustomeTestModel])

    assert detected_migrations.get('drop_tables') == ['POSTTESTMODEL']
    assert detected_migrations.get('create_tables') == []
    assert detected_migrations.get('add_columns') == []
    assert detected_migrations.get('remove_columns') == []


def test_one_column_to_add_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    OldPostTestModel = init_post_test_model_related_to(CustomeTestModel)
    OldPostTestModel.migrate().backend.execute(query=OldPostTestModel.query_creator.sql)

    # add one moore column (title)
    from src.models.model import Model
    from src import fields

    class PostTestModel(Model):
        is_read = fields.BooleanField(null=True)
        id_autor = fields.ForeignKey(related_model=CustomeTestModel)
        content = fields.TextField(null=True)
        title = fields.TextField()

    from src.migrations import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([CustomeTestModel, PostTestModel])

    assert detected_migrations.get('create_tables') == []
    assert detected_migrations.get('drop_tables') == []
    assert len(detected_migrations.get('add_columns')) == 1
    assert detected_migrations.get('add_columns')[0][0] == 'POSTTESTMODEL'
    assert detected_migrations.get('add_columns')[0][1].field_name == 'title'
    assert detected_migrations.get('add_columns')[0][1].__class__.__name__ == 'TextField'
    assert detected_migrations.get('remove_columns') == []


def test_one_column_to_delete_detected(testing_db):
    CustomeTestModel = init_custome_test_model()
    CustomeTestModel.migrate().backend.execute(query=CustomeTestModel.query_creator.sql)

    OldPostTestModel = init_post_test_model_related_to(CustomeTestModel)
    OldPostTestModel.migrate().backend.execute(query=OldPostTestModel.query_creator.sql)

    # delete column autor
    from src.models.model import Model
    from src import fields

    class PostTestModel(Model):
        is_read = fields.BooleanField(null=True)
        content = fields.TextField(null=True)

    from src.migrations import MigrationDetecter
    migration_detecter = MigrationDetecter(CustomeTestModel.query_creator.backend)
    detected_migrations = migration_detecter.get_detected_migrations([CustomeTestModel, PostTestModel])

    assert detected_migrations.get('create_tables') == []
    assert detected_migrations.get('drop_tables') == []
    assert detected_migrations.get('add_columns') == []
    assert len(detected_migrations.get('remove_columns')) == 1
    assert detected_migrations.get('remove_columns')[0][0] == 'POSTTESTMODEL'
    assert detected_migrations.get('remove_columns')[0][1] == 'id_autor'
