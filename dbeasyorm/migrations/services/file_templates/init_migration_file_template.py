from dbeasyorm.migrations.domain.migrations import CreateTableMigration


def render_init_migration_file(migration_model) -> None:
    migration = CreateTableMigration(
        table_name=migration_model.query_creator.get_table_name(),
        fields=migration_model._fields,
    )
    return f'''"""
Migrtion: Init migration
"""
from dbeasyorm.migrations import *
from dbeasyorm.fields import *

def get_migrations():
    return {[migration]}
'''
