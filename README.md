Articles Management System
This Python project offers a robust system for managing authors, articles, and magazines, leveraging a relational database (like PostgreSQL or SQLite) for data persistence. It provides an ORM-like approach through its classes, enabling seamless interaction with the database for creating, reading, updating, and querying various entities.

Features
Add, Query, and Update: Easily manage authors, articles, and magazines.
Query by Association: Retrieve articles by a specific author or magazine.
Detailed Tracking: Keep tabs on author contributions and magazine categories.
Atomic Transactions: Perform multi-step operations (e.g., adding an author with multiple articles) reliably.
Database Management: Includes scripts for schema creation and initial data seeding.
Project Structure
.
├── db/
│   ├── connection.py        # Database connection, schema, and seed functions
├── lib/
│   ├── models/
│   │   ├── author.py        # Author class and DB operations
│   │   ├── article.py       # Article class and DB operations
│   │   ├── magazine.py      # Magazine class and DB operations
├── scripts/
│   ├── run_queries.py       # Sample scripts to query or manipulate data
├── setup_db.py              # Script to create tables and seed initial data
├── test_all.py              # Tests for models and DB integration
├── README.md                # Project documentation
Setup Instructions
Requirements
Python 3.8+
PostgreSQL or SQLite (the current setup uses SQLite by default; see db/connection.py for configuration)
psycopg2-binary (for PostgreSQL) or sqlite3 (built-in for SQLite) Python packages
Install Dependencies
Use pip to install necessary packages. For SQLite, no additional package is needed as it's built-in. For PostgreSQL, you'll install psycopg2-binary:

Bash

pip install psycopg2-binary
Configure Your Database Connection
If you're using PostgreSQL, you'll need to edit db/connection.py to set your database credentials and connection parameters. For SQLite, the default setup will create articles_management.db in your project directory.

How to Use
Set up the database schema and seed initial data:

Bash

python setup_db.py
Run tests to verify everything works as expected:

Bash

python test_all.py
Interact with the database using the models in your Python scripts:

Python

from lib.models.author import Author

author = Author(name="John Doe")
author.save()

articles = author.articles()
print(articles)
Running Queries
You can find and execute predefined queries or scripts in scripts/run_queries.py to explore and manipulate your data.

Contributing
Feel free to open issues or submit pull requests to improve this project. Your contributions are welcome!

License
This project is licensed under the MIT License.