# debug.py

from db.connection import connection, schema, seed
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.scripts import run_queries

def setup_environment():
    print("Setting up schema...")
    schema() 

    print("Seeding database...")
    seed() 

    print("Environment ready. You can now import and test models.")

if __name__ == "__main__":
    setup_environment()

    # Debug:
    print("\nTesting Magazine:")
    magazines = Magazine.find_by_category("Technology")
    for mag in magazines:
        print(mag)

    # Debug: 
    print("\nCreating Author...")
    try:
        author = Author(name="Jane Doe")
        author.save()
        print("Saved:", author)
    except Exception as e:
        print("Error saving author:", e)

    # Debug: 
    print("\nCreating Article...")
    tech_mag = Magazine.find_by_name("Tech Weekly")
    if tech_mag and author.id:
        article = Article(title="The Rise of AI", author_id=author.id, magazine_id=tech_mag.id)
        article.save()
        print("Saved:", article)

    # Run 
    print("\nRunning script queries...")
    run_queries.execute_custom_queries()
