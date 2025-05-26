# lib/db/connection.py

import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    conn = psycopg2.connect(
        dbname="articles_challenge",
        user="titus",
        password="titophil123*",
        cursor_factory=RealDictCursor  # Enables dict-like access to columns
    )
    return conn
