# setup_db.py

from db.connection import connection, schema, seed

def setup_database():
    print("Creating database schema...")
    schema() 

    print("Seeding initial data...")
    seed() 

    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
