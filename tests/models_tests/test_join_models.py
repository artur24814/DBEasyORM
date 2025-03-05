import pytest

from dbeasyorm.query import QueryCreator
from dbeasyorm.migrations import MigrationProcessor
from dbeasyorm.models.exeptions import TheKeyIsNotAForeignKeyError
from faker import Faker

fake = Faker()


def init_related_models():
    from dbeasyorm.models.model import Model
    from dbeasyorm import fields

    class UserModel(Model):
        name = fields.TextField()
        second_name = fields.TextField()
        email = fields.TextField(unique=True)

    class UsersPostModel(Model):
        autor = fields.ForeignKey(related_model=UserModel, null=True)
        content = fields.TextField(null=True)

    class UserComment(Model):
        post = fields.ForeignKey(related_model=UsersPostModel, null=True)
        autor = fields.ForeignKey(related_model=UserModel, null=True)

    migration_exec = MigrationProcessor(db_backend=UserModel.query_creator.backend)

    DETECTED_MIGRATIONS = {
        "create_tables": [UserModel, UsersPostModel, UserComment],
        "add_columns": [],
        "drop_tables": [],
        "remove_columns": []
    }
    migration_exec.execute_detected_migration(detected_migration=DETECTED_MIGRATIONS)

    return UserModel, UsersPostModel, UserComment


def test_joining_midels_and_reduse_amount_of_queryes(testing_db):
    UserModel, UsersPostModel, UserComment = init_related_models()

    for _ in range(10):
        UserModel(name=fake.name(), second_name=fake.last_name(), email=fake.email()).save().execute()
    user = UserModel.query_creator.all().execute()[5]
    UsersPostModel(autor=user, content=fake.text()).save().execute()
    post = UsersPostModel.query_creator.all().execute()[0]
    UserComment(autor=user, post=post).save().execute()

    with QueryCreator.query_counter:
        usercomment = UserComment.query_creator.all().execute()[0]
        assert usercomment.autor.name == user.name
        assert usercomment.post.content == post.content
        assert QueryCreator.query_counter.get_query_count() == 3

    with QueryCreator.query_counter:
        usercomment_with_join_autor = UserComment.query_creator.all().join("autor").execute()[0]
        assert usercomment_with_join_autor.autor.name == user.name
        assert usercomment_with_join_autor.post.content == post.content
        assert QueryCreator.query_counter.get_query_count() == 2

    with QueryCreator.query_counter:
        usercomment_with_join_autor_and_post = UserComment.query_creator.all().join("autor").join("post").execute()[0]
        assert usercomment_with_join_autor_and_post.autor.name == user.name
        assert usercomment_with_join_autor_and_post.post.content == post.content
        assert QueryCreator.query_counter.get_query_count() == 1


def test_ForeignKeyError_when_we_put_wrong_field(testing_db):
    UserModel, UsersPostModel, UserComment = init_related_models()

    for _ in range(10):
        UserModel(name=fake.name(), second_name=fake.last_name(), email=fake.email()).save().execute()
    user = UserModel.query_creator.all().execute()[5]
    UsersPostModel(autor=user, content=fake.text()).save().execute()
    post = UsersPostModel.query_creator.all().execute()[0]
    UserComment(autor=user, post=post).save().execute()

    with pytest.raises(TheKeyIsNotAForeignKeyError):
        usercomment_with_join_fake_field = UserComment.query_creator.all().join("comment").execute()
        assert len(usercomment_with_join_fake_field) == 0
