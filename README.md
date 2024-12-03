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
``` -->
## 🔧 Usage

1. Connect to the Database
```python
from DBEasyORM import connect

# Establish a connection
connection = connect(
    db_type='postgresql',
    host='localhost',
    database='mydatabase',
    user='username',
    password='password'
)
```

2. Define Models
```python
from DBEasyORM.models.model import Model
from DBEasyORM.DB_fields.fields import Integer, String

class User(Model):
    name = String(max_length=100)
    email = String(max_length=100, unique=True)
```

3. Perform CRUD Operations
```python
# Create a new user
new_user = User(name='John Doe', email='john@example.com')
new_user.save().execute()

# Fetch all users
users = User.all().execute()

# Update a user
user = User.get_one(1).execute()
user.name = 'Jane Doe'
user.save()

# Delete a user
user.delete()
```

4. Migrations
```
bash
$ python migrations.py run
```
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

## 🧪 Testing
To run tests:

```bash
Skopiuj kod
pytest tests/
```
We recommend testing on multiple database types to ensure compatibility.

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
