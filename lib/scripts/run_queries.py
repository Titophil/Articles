from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.connection import CURSOR, CONN

def reset_tables():
    CURSOR.execute("DELETE FROM articles;")
    CURSOR.execute("DELETE FROM authors;")
    CURSOR.execute("DELETE FROM magazines;")
    CONN.commit()

def create_sample_data():
    # Create magazine
    magazine1 = Magazine(name="Nature World", category="Science")
    magazine1.save()

    magazine2 = Magazine(name="History Daily", category="History")
    magazine2.save()

    # Create authors
    author1 = Author(name="Charles Darwin")
    author1.save()

    author2 = Author(name="Marie Curie")
    author2.save()

    author3 = Author(name="Yuval Harari")
    author3.save()

    # Create articles
    article1 = Article(title="Evolution Theory", author_id=author1.id, magazine_id=magazine1.id)
    article1.save()

    article2 = Article(title="Natural Selection", author_id=author1.id, magazine_id=magazine1.id)
    article2.save()

    article3 = Article(title="Radiation Research", author_id=author2.id, magazine_id=magazine1.id)
    article3.save()

    article4 = Article(title="Sapiens Review", author_id=author3.id, magazine_id=magazine2.id)
    article4.save()

    return {
        "authors": [author1, author2, author3],
        "magazines": [magazine1, magazine2],
        "articles": [article1, article2, article3, article4]
    }

def run_tests():
    print("\n=== RESETTING DATABASE ===")
    reset_tables()

    print("\n=== CREATING SAMPLE DATA ===")
    data = create_sample_data()

    print("\n=== AUTHOR TESTS ===")
    for author in data["authors"]:
        print(f"\nAuthor: {author}")
        print("Articles:")
        for article in author.articles():
            print(f" - {article}")
        print("Magazines:")
        for magazine in author.magazines():
            print(f" - {magazine}")

    print("\n=== MAGAZINE TESTS ===")
    for magazine in data["magazines"]:
        print(f"\nMagazine: {magazine}")
        print("Articles:")
        for article in magazine.articles():
            print(f" - {article}")
        print("Contributors:")
        for contributor in magazine.contributors():
            print(f" - {contributor}")
        print("Article Titles:")
        for title in magazine.article_titles():
            print(f" - {title}")
        print("Contributing Authors (more than 2 articles):")
        for ca in magazine.contributing_authors():
            print(f" - {ca}")

    print("\n=== ARTICLE TESTS ===")
    for article in data["articles"]:
        print(f"\nArticle: {article}")
        print(f"Author: {article.author()}")
        print(f"Magazine: {article.magazine()}")

if __name__ == "__main__":
    run_tests()
