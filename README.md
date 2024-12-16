# DBEasyORM: Simplified ORM for SQL Databases

Streamlined Object-Relational Mapping for Python and SQL Databases.

## 🚀 About the Project
DBEasyORM is a lightweight and intuitive Object-Relational Mapping (ORM) library designed to simplify interactions between Python applications and SQL databases. By mapping Python objects to SQL tables, DBEasyORM eliminates the need for complex raw SQL queries, enabling developers to focus on writing clean, maintainable, and efficient code.

With built-in support for model definitions, queries, migrations, and transactions, DBEasyORM makes database operations seamless for beginners and experts alike.

## 🛠️ Features
* Database Connection: Connect to PostgreSQL, MySQL, SQLite, and other SQL databases with ease.
* Model Definition: Map Python classes to SQL tables with field types, constraints, and relationships.
* CRUD Operations: Create, read, update, and delete records without writing raw SQL.
* Querying API: Perform complex queries using filter, order, limit, and chaining methods.
* Migrations: Automatically generate and apply schema changes with simple commands.
* Transaction Management: Handle atomic database operations with robust transaction support.
* Relationships: Define and query one-to-many and many-to-many relationships.
* Custom Validation: Add custom field-level validation to enforce business rules.

<!-- ## 📦 Installation
You can install DBEasyORM via pip:

```bash
pip install DbEasyORM
```

Or install development dependencies. Use the following commands:

```bash
pip install DBEasyORM[dev]
``` -->
## 🔧 Usage

1. Connect to the Database

   ### 📄 Configuration File Recommendation
   We recommend using a configuration file (e.g., `dbeasyorm.ini`) to streamline and centralize the setup of your database and application parameters. Below is an example of a `dbeasyorm.ini` file:

    ```ini
    [database]
    db_type = sqlite
    database_path = db.sqlite3

    [app]
    dir = app
    ```
    `[database]`: This section is used to specify the database parameters:

    `db_type`: The type of database (e.g., sqlite, postgres).
    `database_path`: The path to the SQLite database file or other database connection details (e.g., `host` and `port` for PostgreSQL).

    `[app]`: This section specifies the application settings:

    `dir`: The folder where the models are stored. This is used for generating database migrations.


    By using a configuration file, you can simplify the process of managing database connections and app-specific settings, especially when working in different environments (e.g., development, testing, production).

    ### Use function

    #### PostgreSQL Example:

    For PostgreSQL, ensure that the PostgreSQL service is running and the database and user credentials are correct.
    You can initialize a PostgreSQL database by connecting to an existing database or creating 
    a new one using PostgreSQL’s command-line tools or a GUI like pgAdmin.

    ```python
    from DBEasyORM import set_database_backend

    # set Postgres as database backend
    set_database_backend(
        "postgresql",
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    ```

    #### sqlite Example:

    in the case of sqlite, if the database does not exist, it will be created automatically

    ```python
    from DBEasyORM import set_database_backend

    # set sqlite as database backend
    set_database_backend("sqlite", database_path="my_database.sqlite")
    ```

2. Define Models
    ```python
    from DBEasyORM.models.model import Model
    from DBEasyORM.DB_fields import fields

    class User(Model):
        name = fields.TextField()
        email = fields.TextField(unique=True)
        is_admin = fields.BooleanField(null=True)
        age = fields.IntegerField(min=0)
        salary = fields.FloatField(null=True)
    ```

3. Migrations

    Once you have defined your models, perform migrations:
    ```bash
    $ python migrations.py run
    ```

    all arguments:

    ```bash
    $ dbeasyorm update-database --help              
    usage: cli.py update-database [-h] [-l LOOCKUP_FOLDER] [-i ID_MIGRATIONS] [-r] [-c CONFIG]

    options:
        -l LOOCKUP_FOLDER, --loockup-folder Path to the lookup folder
        -i ID_MIGRATIONS, --id-migrations ID of specific migrations
        -r, --restore   Restore database to the previous state
        -c CONFIG, --config  Path to the config.ini file
    ```

4. Perform CRUD Operations

* Create New Models
    #### Using save Method
    The save method allows you to create a new model instance and persist it to the database. Example:

    ```python
    # Create a new instance and generate quey
    new_test_model = User(
        name="John Doe",
        email="john@example.com",
        age=30
    )
    
    new_test_model.save()

    # Verify the instance
    assert new_test_model.id == -1
    assert new_test_model.query_creator.return_id is True

    # Execute query and create the instance
    returned_value = new_test_model.query_creator.execute()
    assert returned_value == 1
    ```
    #### Using create Method
    The create method simplifies model instantiation and saving in a single step. Example:

    ```python
    # Create and save a new model
    instance_id = User.query_creator.create(
        name="Jon",
        email="jon@example.com",
        age=34,
        is_admin=1,
        salary=13.000
    ).execute()

    # Verify the ID
    assert instance_id == 1
    ```

* Read Models
    #### Fetch All Instances

    Retrieve all instances of a model using the all query.

    ```python
    # Fetch all existing instances
    queryset = User.query_creator.all().execute()
    assert len(queryset) == 0

    # Add and retrieve instances
    new_test_model1 = User(
        name="Model1",
        email="test1@example.com",
        age=34,
        is_admin=1,
        salary=13.000
    )
    new_test_model1.save().execute()

    new_test_model2 = User(
        name="Model2",
        email="test2@example.com",
        age=41,
        is_admin=0,
        salary=7.000
    )
    new_test_model2.save().execute()

    queryset = User.query_creator.all().execute()
    assert len(queryset) == 2
    assert isinstance(queryset[0], User)
    ```
    #### Filter Instances

    Filter models based on specific attributes:

    ```python
    from faker import Faker
    import random

    fake = Faker()

    def create_custome_test_model(name=None, email=None, salary=None):
        return User(
            name=name if name else fake.name(),
            email=email if email else fake.email(),
            is_admin=random.choice([0, 1]),
            age=random.randint(15, 45),
            salary=salary if salary else round(random.uniform(5.000, 15.000), 3)
        )

    # Create test models
    for _ in range(10):
        create_custome_test_model(name="Test").save().execute()

    for _ in range(15):
        create_custome_test_model(salary=12.00).save().execute()

    # Filter by name
    queryset_name = User.query_creator.filter(name="Test").execute()
    assert len(queryset_name) == 10

    # Filter by salary
    queryset_salary = User.query_creator.filter(salary=12.00).execute()
    assert len(queryset_salary) == 15
    ```
    #### Fetch a Single Instance

    Retrieve a single instance matching a condition:

    ```python
    # Create test models
    create_custome_test_model(name="Test").save().execute()
    create_custome_test_model(salary=12.00).save().execute()

    # Get one instance by attribute
    queryset_name = User.query_creator.get_one(name="Test").execute()
    assert isinstance(queryset_name, User)

    # Handle non-existent instance
    import pytest
    from src.query import TheInstanceDoesNotExistExeption

    with pytest.raises(TheInstanceDoesNotExistExeption):
        User.query_creator.get_one(name="NonExistent").execute()
    ```
* Update Models

    Update Attributes of Existing Models
    To modify a model, update its attributes and call `save`:

    ```python
    # Create and retrieve a model
    User.query_creator.create(
        name="Old Name",
        email="test2@example.com",
        age=41,
        is_admin=0,
        salary=7.000
    ).save().execute()

    model = User.query_creator.all().execute()[0]

    # Update the name
    model.name = "Updated Name"
    model.save().execute()

    # Verify the update
    updated_model = User.query_creator.all().execute()[0]
    assert updated_model.name == "Updated Name"
    ```
* Delete Models.

    Delete a Specific Model
    To delete a specific instance:

    ```python
    # Create and fetch instances
    User.query_creator.create(
        name="Jon",
        email="test2@example.com",
        age=41,
        is_admin=0,
        salary=7.000
    ).save().execute()
    model = User.query_creator.all().execute()[0]

    # Delete the instance
    model.delete().execute()

    # Verify deletion
    queryset_after_delete = User.query_creator.all().execute()
    assert len(queryset_after_delete) == 0
    ```

## 🛠️ Customization

#### Creating a Custom Database Engine
If DBEasyORM doesn't support your database or you need special functionality, you can easily create a custom database engine. To do this, subclass the DataBaseBackend class and implement the necessary methods.

Example: Custom Database Engine

1. Create custome backend
```python
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
```
2. Use this backend
```python
# add this db into registered database
from DBEasyORM import register_backend

register_backend("custom", CustomDatabaseBackend)

# Use this backend for your purpose
set_database_backend("custom", custom_param="value")
```

DBEasyORM allows developers to define custom fields to meet specific requirements. Here's an example of how to create a custom field:

Example: Custom Field Creation
```python
from DBEasyORM.DB_fields.abstract import BaseField

class PercentageField(BaseField):
    def __init__(self, field_name=None, null=False, primary=False, unique=False, min=0, max=100):
        super().__init__(float, field_name, null, primary, unique)
        self.min = min
        self.max = max

    def get_basic_sql_line(self) -> str:
        return f"{self.field_name} REAL"

    def validate(self, value) -> None:
        super().validate(value)
        if not (self.min <= value <= self.max):
            raise ValueError(f"Value for field '{self.field_name}' must be between {self.min} and {self.max}.")
```
You can now use this custom field in your models like any other field:

```python
class Product(Model):
    discount = PercentageField()
```

## ⚡ Optimization Goals
To help developers optimize database interactions, DBEasyORM includes tools like the `QueryCounter` from the `QueryCreator` module. This tool tracks and logs database queries, making it easier to analyze and reduce redundant queries for better performance.

Example Usage of `QueryCounter`:
```python
from src.query import QueryCreator
from DBEasyORM.models.model import Model
from DBEasyORM.DB_fields import fields

class User(Model):
    name = fields.TextField()
    email = fields.TextField(unique=True)

with QueryCreator.query_counter:
    for 1 in range(10):
        User(name=f"Test{i}", email=f"test{i}@examlpe.com").save().execute()

    assert QueryCreator.query_counter.get_query_count() == 10

with QueryCreator.query_counter:
    for _ in range(10, 25):
        User(name=f"Test{i}", email=f"test{i}@examlpe.com").save().execute()
    assert QueryCreator.query_counter.get_query_count() == 15

with QueryCreator.query_counter:
    User.query_creator.all().execute()
    assert QueryCreator.query_counter.get_query_count() == 1
```

#### Using QueryCounter as a Query Logger
The `QueryCounter` can also be used as a logger to review database queries, their count, and execution time. This feature is particularly useful for optimizing query-heavy operations:

```python
from src.query import QueryCreator  

with QueryCreator.query_counter:
    # Perform database operations
    for 1 in range(10):
        User(name=f"Test{i}", email=f"test{i}@examlpe.com").save().execute()
```
terminal:
```bash
Query logging started. Previous logs cleared.
Query logging ended. Total queries: 10
Queries:
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
INSERT INTO USER (name, email) VALUES (?, ?)
Elapsed time: 0.08 seconds.
```
By using `QueryCounter`, developers can identify unnecessary or repetitive queries and fine-tune their database interactions to achieve better performance.

## 🧪 Use DBEasyORM for Testing purpose with pytest
To testesting with pytest, you can use fixtures to create temporary databases for testing purposes. Below is an example configuration that uses SQLite as the test database. This setup ensures that each test gets a fresh database to work with.

Example Configuration for Testing
1. Create a conftest.py file in your tests directory to set up the testing environment.

conftest.py Example:
```python
import pytest
import tempfile

from src import set_database_backend


@pytest.fixture
def testing_db():
    # Create a temporary SQLite database
    _, db_path = tempfile.mkstemp()
    
    # Set the SQLite backend for the tests
    set_database_backend("sqlite", database_path=db_path)
    
    # Yield the database path to be used in the tests
    yield db_path
```
2. Configuring pytest
To use the testing_db fixture in your tests, make sure to install pytest if you haven't already:

```bash
pip install pytest
```
In your test files, you can now use the testing_db fixture to set up the database for each test:

3. Test Example:
```python
from DBEasyORM import Model, fields

class User(Model):
    username = fields.TextField(null=True)
    email = fields.TextField(unique=True)
    age = fields.IntegerField(min=0)

def test_user_creation(testing_db):
    # Create a new user
    new_user = User(username='Test User', email='testuser@example.com', age=25)
    new_user.save().execute()

    # Verify that the user was saved
    users = User.all().execute()
    assert len(users) == 1
    assert users[0].username == 'Test User'
    assert users[0].email == 'testuser@example.com'
```
Running Tests
To run your tests with pytest, simply execute the following command in your terminal:

```bash
pytest
```
This setup ensures that each test runs in an isolated environment with a temporary SQLite database that gets cleaned up after each test run.

## 📚 Documentation
Check out the Full Documentation for a complete guide on using DBEasyORM, including advanced querying, relationships, and configurations.

## 🤝 Contributing
We welcome contributions to improve DBEasyORM! To contribute, please:

1. Fork the repository.
2. Create a feature branch (git checkout -b feature-name).
3. Commit your changes (git commit -m "Add feature-name").
4. Push to the branch (git push origin feature-name).
5. Open a Pull Request.
See our CONTRIBUTING.md for detailed guidelines.

## 🧪 Testing and Development

If you wish to contribute to DBEasyORM or run its test suite, 
you need to install development dependencies. Use the following commands:

```bash
pip install DbEasyORM[dev]
```
To run the tests:

```bash
pytest
```

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 🛤️ Roadmap
* Add support for additional SQL dialects (e.g., Oracle, SQL Server).
* Implement advanced query features like subqueries and joins.
* Add indexing and performance tuning options.
* Improve logging and error reporting.

## 🗨️ Community
Join the DBEasyORM community for discussions and updates:

GitHub Issues
Discussions

## 📢 Acknowledgments
Thanks to the open-source community for inspiring and supporting this project!
