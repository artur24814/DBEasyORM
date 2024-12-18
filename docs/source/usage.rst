.. _usage:

=============
Usage Guide
=============

This document provides detailed instructions on how to use the DBEasyORM library for database management and interaction.

.. contents::
   :local:
   :depth: 2

---------------------
1. Connect to the Database
---------------------

Configuration File Recommendation
------------------------------------

To simplify database and application parameter setup, we recommend using a configuration file, e.g., ``dbeasyorm.ini``:

.. code-block:: ini

    [database]
    db_type = sqlite
    database_path = db.sqlite3

    [app]
    dir = app

**Configuration Details:**

- **[database]:**
  - **db_type**: Specifies the database type (e.g., sqlite, postgres).
  - **database_path**: Path to the SQLite database file or connection details for other databases.

- **[app]:**
  - **dir**: Directory containing your models (used for migrations).

Using a configuration file centralizes settings management across environments (development, testing, production).

Using the `set_database_backend` Function
------------------------------------

PostgreSQL Example
~~~~~~~~~~~~~~~~~~

Ensure the PostgreSQL service is running, and the database credentials are correct:

.. code-block:: python

    from DBEasyORM import set_database_backend

    set_database_backend(
        "postgresql",
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword"
    )

SQLite Example
~~~~~~~~~~~~~~

SQLite databases are created automatically if they do not already exist:

.. code-block:: python

    from DBEasyORM import set_database_backend

    set_database_backend("sqlite", database_path="my_database.sqlite")


---------------------
2. Define Models
---------------------

Create models using the ``Model`` class and define fields:

.. code-block:: python

    from DBEasyORM.models.model import Model
    from DBEasyORM.DB_fields import fields

    class User(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField(min=0)
        salary = fields.FloatField(null=True)


---------------------
3. Migrations
---------------------

Perform migrations to update the database schema:

.. code-block:: bash

    $ dbeasyorm update-database

**Available Options:**

.. code-block:: bash

    $ dbeasyorm update-database --help

    usage: cli.py update-database [-h] [-l LOOCKUP_FOLDER] [-i ID_MIGRATIONS] [-r] [-c CONFIG]

    options:
        -l, --loockup-folder   Path to the lookup folder
        -i, --id-migrations    ID of specific migrations
        -r, --restore          Restore database to the previous state
        -c, --config           Path to the config.ini file


---------------------
4. Perform CRUD Operations
---------------------

Create
-------

Using the `save` Method:
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    new_user = User(name="John Doe", email="john@example.com", age=30)
    new_user.save()

Using the `create` Method:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    User.query_creator.create(
        name="Jon",
        email="jon@example.com",
        age=34
    ).execute()

Read
----

Fetch All Instances:
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    queryset = User.query_creator.all().execute()

Filter Instances:
~~~~~~~~~~~~~~~~~

.. code-block:: python

    queryset = User.query_creator.filter(name="Test").execute()

Fetch a Single Instance:
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    user = User.query_creator.get_one(name="Test").execute()

Update
-------

Modify attributes and call `save`:

.. code-block:: python

    user = User.query_creator.all().execute()[0]
    user.name = "Updated Name"
    user.save().execute()

Delete
-------

Delete specific instances:

.. code-block:: python

    user = User.query_creator.all().execute()[0]
    user.delete().execute()


---------------------
🛠️ Customization
---------------------

Create a Custom Database Engine
-------------------------------

Subclass the ``DataBaseBackend`` class to implement a custom engine:

.. code-block:: python

    from DBEasyORM.db.backends import DataBaseBackend

    class CustomDatabaseBackend(DataBaseBackend):
        def __init__(self, connection_str):
            self.connection_str = connection_str
            # ...

Create a Custom Field
----------------------

Define custom fields by subclassing the ``BaseField`` class:

.. code-block:: python

    from DBEasyORM.DB_fields.abstract import BaseField

    class PercentageField(BaseField):
        def __init__(self, field_name=None, null=False, primary=False, unique=False, min=0, max=100):
            super().__init__(float, field_name, null, primary, unique)
            self.min = min
            self.max = max


---------------------
⚡ Optimization Goals
---------------------

QueryCounter
-------------

Track and analyze query execution:

.. code-block:: python

    from src.query import QueryCreator

    with QueryCreator.query_counter:
        User.query_creator.all().execute()
        print(QueryCreator.query_counter.get_query_count())

Resolving the N+1 Query Problem
-------------------------------

Optimize queries by using ``join``:

.. code-block:: python

    user_comments = UserComment.query_creator.all().join("autor").join("post").execute()


---------------------
🧪 Testing with pytest
---------------------

Configure Testing Database
--------------------------

Use pytest fixtures to set up a temporary SQLite database for testing:

.. code-block:: python

    import pytest
    import tempfile
    from src import set_database_backend

    @pytest.fixture
    def testing_db():
        _, db_path = tempfile.mkstemp()
        set_database_backend("sqlite", database_path=db_path)
        yield db_path

Example Test Case:
------------------

.. code-block:: python

    def test_user_creation(testing_db):
        new_user = User(username="Test User", email="testuser@example.com", age=25)
        new_user.save().execute()
        users = User.all().execute()
        assert len(users) == 1

Run tests:

.. code-block:: bash

    pytest
