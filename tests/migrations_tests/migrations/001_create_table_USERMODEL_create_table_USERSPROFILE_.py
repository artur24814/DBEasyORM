"""
Migration: create_table_USERMODEL_create_table_USERSPROFILE_
Created: 2025-03-13 13:42:48.065845
"""

from dbeasyorm.migrations import *
from dbeasyorm.fields import *


def get_migrations():
    return [
        CreateTableMigration(
            table_name="USERMODEL",
            fields={
                "_id": IntegerField(
                    field_name="_id",
                    null=False,
                    primary=True,
                    unique=False,
                    autoincrement=True,
                    default=None,
                    min=None,
                    max=None,
                ),
                "name": TextField(
                    field_name="name",
                    null=False,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "second_name": TextField(
                    field_name="second_name",
                    null=False,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "email": TextField(
                    field_name="email",
                    null=False,
                    primary=False,
                    unique=True,
                    autoincrement=False,
                    default=None,
                ),
                "age": IntegerField(
                    field_name="age",
                    null=False,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                    min=None,
                    max=None,
                ),
                "salary": FloatField(
                    field_name="salary",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "salary2": FloatField(
                    field_name="salary2",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
            },
        ),
        CreateTableMigration(
            table_name="USERSPROFILE",
            fields={
                "_id": IntegerField(
                    field_name="_id",
                    null=False,
                    primary=True,
                    unique=False,
                    autoincrement=True,
                    default=None,
                    min=None,
                    max=None,
                ),
                "id_autor": ForeignKey(
                    field_name="id_autor",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                    related_model="USERMODEL",
                    on_delete="CASCADE",
                ),
                "bio": TextField(
                    field_name="bio",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
            },
        ),
        CreateTableMigration(
            table_name="USERSPOSTMODEL",
            fields={
                "_id": IntegerField(
                    field_name="_id",
                    null=False,
                    primary=True,
                    unique=False,
                    autoincrement=True,
                    default=None,
                    min=None,
                    max=None,
                ),
                "is_read": BooleanField(
                    field_name="is_read",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "id_autor": ForeignKey(
                    field_name="id_autor",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                    related_model="USERMODEL",
                    on_delete="CASCADE",
                ),
                "content": TextField(
                    field_name="content",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "title": TextField(
                    field_name="title",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
            },
        ),
    ]
