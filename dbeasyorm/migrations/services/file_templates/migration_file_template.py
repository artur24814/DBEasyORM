import datetime


def render_migration_file(migration_name: str, migrations: dict):
    return f'''"""
Migrtion: {migration_name}
Created: {datetime.datetime.now()}
"""
from dbeasyorm.migrations import *
from dbeasyorm.fields import *

def get_migrations():
    return {migrations}
'''
