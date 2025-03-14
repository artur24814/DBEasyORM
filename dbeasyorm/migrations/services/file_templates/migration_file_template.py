import datetime


def render_migration_file(migration_name: str, migrations: list):
    return f'''"""
Migration: {migration_name}
Created: {datetime.datetime.now()}
"""
from dbeasyorm.migrations import *
from dbeasyorm.fields import *

def get_migrations():
    return {migrations}
'''
