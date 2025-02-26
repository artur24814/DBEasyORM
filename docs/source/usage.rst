.. _usage:

=============
Usage Guide
=============

This document provides detailed instructions on how to use the DBEasyORM library for database management and interaction.

.. contents::
   :local:
   :depth: 2

----------------
Getting Started
----------------

1. Connect to the Database
---------------------

Configuration File Recommendation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **PostgreSQL Example**

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

    **SQLite Example**

    SQLite databases are created automatically if they do not already exist:

    .. code-block:: python

        from DBEasyORM import set_database_backend

        set_database_backend("sqlite", database_path="my_database.sqlite")


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
Perform CRUD Operations
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


--------------------------------
Operators for Query Filtering
--------------------------------

This library provides various SQL operators for filtering data.

**Available Operators:**

Between:
--------
Filters values within a given range.

.. code-block:: python

    from your_module import CustomeTestModel

    # Create test records
    for i in range(10):
        CustomeTestModel(name=f"User{i}", age=14 + i, salary=1000.0 + i * 10).save().execute()

    # Filtering using BetweenSQLOperator
    query = CustomeTestModel.query_creator.filter(age__between=(18, 60))
    print(query.sql)  # Output: SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE age BETWEEN 18 AND 60
    result = query.execute()
    assert len(result) == 6

In
----

Filters values that exist in a given list.

.. code-block:: python

    from your_module import CustomeTestModel

    # Create test records
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    for name in names:
        CustomeTestModel(name=name).save().execute()

    # Filtering using InSQLOperator
    query = CustomeTestModel.query_creator.filter(name__in=["Alice", "Charlie", "Eve"])
    print(query.sql)  # Output: SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE name IN ('Alice', 'Charlie', 'Eve')
    result = query.execute()
    assert len(result) == 3

StartsWith
----------

Filters values that start with a specific substring.

.. code-block:: python

    from your_module import CustomeTestModel

    # Create test records
    names = ["Jon", "Tom", "Jonathan", "James", "Bill"]
    for name in names:
        CustomeTestModel(name=name).save().execute()

    # Filtering using StartsWithSQLOperator
    query = CustomeTestModel.query_creator.filter(name__startswith="Jo")
    print(query.sql)  # Output: SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE name LIKE 'Jo%'
    result = query.execute()
    assert len(result) == 2

EndsWith
--------

Filters values that end with a specific substring.

.. code-block:: python

    from your_module import CustomeTestModel

    # Create test records
    names = ["Jon", "Tom", "Jonathan", "James", "Bill"]
    for name in names:
        CustomeTestModel(name=name).save().execute()

    # Filtering using EndsWithSQLOperator
    query = CustomeTestModel.query_creator.filter(name__endswith="n")
    print(query.sql)  # Output: SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE name LIKE '%n'
    result = query.execute()
    assert len(result) == 2

---------------------
🛠️ Customization
---------------------

Create a Custom Database Engine
-------------------------------

If DBEasyORM doesn't support your database or you need special functionality, you can easily create a custom database engine.
To do this, subclass the DataBaseBackend class and implement the necessary methods.

1. Create custome backend

Subclass the ``DataBaseBackend`` class to implement a custom engine:

.. code-block:: python

    from DBEasyORM.db.backends import DataBaseBackend


    class CustomDatabaseBackend(DataBaseBackend):
        def __init__(self, connection_str: str):
            self.connection_str = connection_str
            self.connection = None

            # NOTE: This map is needed for validating base fields,
            # and for migrations based on python types it will map them to SQL types
            self.type_map = self.get_sql_types_map()

        def get_placeholder(self) -> str:
            return ":"

        def get_sql_type(self, type):
            # Define how each Python type maps to your custom SQL type
            return "CUSTOM_TYPE"

        def get_sql_types_map(self) -> dict:
            # NOTE: This map is needed for validating base fields,
            # and for migrations based on python types it will map them to SQL types
            return {
                int: "CUSTOM_INT",
                str: "CUSTOM_TEXT",
                float: "CUSTOM_REAL"
            }

        def connect(self, *args, **kwargs):
            # Implement your custom connection logic
            pass

        def execute(self, query: str, params=None):
            # Implement how queries are executed
            pass

        def generate_select_sql(self, table_name: str, columns: tuple, where_clause: tuple, limit: int = None, offset: int = None) -> str:
            # Implement generation custome query for select
            pass

        def generate_update_sql(self, table_name: str, set_clause: tuple, where_clause: tuple) -> str:
            # Implement generation custome update for select
            pass

        def generate_delete_sql(self, table_name: str, where_clause: tuple) -> str:
            # Implement generation custome delet for select
            pass
2. Use this backend

.. code-block:: python

    # add this db into registered database
    from DBEasyORM import register_backend

    register_backend("custom", CustomDatabaseBackend)

    # Use this backend for your purpose
    set_database_backend("custom", custom_param="value")

Create a Custom Field
----------------------
DBEasyORM allows developers to define custom fields to meet specific requirements. Here's an example of how to create a custom field:

Define custom fields by subclassing the ``BaseField`` class:

.. code-block:: python

    from DBEasyORM.DB_fields.abstract import BaseField

    class PercentageField(BaseField):
        def __init__(self, field_name=None, null=False, primary=False, unique=False, min=0, max=100):
            super().__init__(float, field_name, null, primary, unique)
            self.min = min
            self.max = max

You can now use this custom field in your models like any other field:

.. code-block:: python

    class Product(Model):
        discount = PercentageField()


Creating a Custom Operator
--------------------------
You can extend the operator functionality by creating your own custom SQL operator.

Example: Creating a Custom AdminPrefixSQLOperator

.. code-block:: python

    from .abstract import OperatorSQLABC

    class AdminPrefixSQLOperator(OperatorSQLABC):
        operator_name = "admin_prefix"

        def apply(self, col=None, value=None, *args, **kwargs) -> str:
            return f"{col} LIKE 'admin_%'"

Registering the Custom Operator

.. code-block:: python

    from your_module.operator_registry import register_operator
    from your_module.custom_operators import AdminPrefixSQLOperator

    register_operator("admin_prefix", AdminPrefixSQLOperator)

Using the Custom Operator

.. code-block:: python

    query = CustomeTestModel.query_creator.filter(username__admin_prefix=True)
    print(query.sql)  
    # Output: SELECT CUSTOMETESTMODEL.* FROM CUSTOMETESTMODEL WHERE username LIKE 'admin_%'

    result = query.execute()

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
