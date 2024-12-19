# DBEasyORM: Simplified ORM for SQL Databases

Streamlined Object-Relational Mapping for Python and SQL Databases.

## About the Project
DBEasyORM is a lightweight and intuitive Object-Relational Mapping (ORM) library designed to simplify interactions between Python applications and SQL databases. By mapping Python objects to SQL tables, DBEasyORM eliminates the need for complex raw SQL queries, enabling developers to focus on writing clean, maintainable, and efficient code.

With built-in support for model definitions, queries, migrations, and transactions, DBEasyORM makes database operations seamless for beginners and experts alike.

## Features
* **Database Connection**: Connect to PostgreSQL, MySQL, SQLite, and other SQL databases with ease.
* **Model Definition**: Map Python classes to SQL tables with field types, constraints, and relationships.
* **CRUD Operations**: Create, read, update, and delete records without writing raw SQL.
* **Querying API**: Perform complex queries using filter, order, limit, and chaining methods.
* **Migrations**: Automatically generate and apply schema changes with simple commands.
* **Transaction Management**: Handle atomic database operations with robust transaction support.
* **Relationships**: Define and query one-to-many and many-to-many relationships.
* **Custom Validation**: Add custom field-level validation to enforce business rules.

## Installation
You can install DBEasyORM via pip:

```bash
pip install dbeasyorm
```

Or install development dependencies. Use the following commands:

```bash
pip install dbeasyorm[dev]
```

## Documentation
Check out the <a href="https://dbeasyorm.readthedocs.io/en/latest/index.html">Full Documentation</a> for a complete guide on using DBEasyORM, including advanced querying, relationships, and configurations.
