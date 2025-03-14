"""
Migrtion: Init migration
"""

from dbeasyorm.migrations import *
from dbeasyorm.fields import *


def get_migrations():
    return [
        CreateTableMigration(
            table_name="MIGRATIONMODEL",
            fields={
                "_id": IntegerField(
                    field_name="_id",
                    null=False,
                    primary=True,
                    unique=True,
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
                "status": IntegerField(
                    field_name="status",
                    null=False,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=0,
                    min=None,
                    max=None,
                ),
                "applied_at": TextField(
                    field_name="applied_at",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
                "hash": TextField(
                    field_name="hash",
                    null=True,
                    primary=False,
                    unique=False,
                    autoincrement=False,
                    default=None,
                ),
            },
        )
    ]
