from ..db.connection import CONN, CURSOR
class Author:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = value.strip()

    @classmethod
    def add_author_with_articles(cls, author_name, articles_data):
        """
        Add an author and their articles in a single transaction.
        articles_data: list of dicts with keys 'title' and 'magazine_id'.
        """
        try:
            CONN.autocommit = False
            CURSOR.execute(
                "INSERT INTO authors (name) VALUES (%s) RETURNING id",
                (author_name,)
            )
            author_id = CURSOR.fetchone()[0]

            for article in articles_data:
                CURSOR.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (%s, %s, %s)",
                    (article['title'], author_id, article['magazine_id'])
                )

            CONN.commit()
            return True
        except Exception as e:
            CONN.rollback()
            print(f"Transaction failed: {e}")
            return False
        finally:
            CONN.autocommit = True

    def save(self):
        sql = """INSERT INTO authors (name) VALUES (%s) RETURNING id"""
        CURSOR.execute(sql, (self.name,))
        self.id = CURSOR.fetchone()[0]
        CONN.commit()
        Author.all[self.id] = self

    @classmethod
    def instance_from_db(cls, row):
        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1], id=row[0])
            cls.all[author.id] = author
        return author

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM authors WHERE id = %s"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM authors WHERE name = %s"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_all(cls):
        sql = "SELECT * FROM authors"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def top_author_by_articles(cls):
        CURSOR.execute("""
            SELECT au.id, au.name, COUNT(a.id) AS article_count
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            GROUP BY au.id
            ORDER BY article_count DESC
            LIMIT 1;
        """)
        row = CURSOR.fetchone()
        if row:
            author = cls(id=row[0], name=row[1])
            return author, row[2]
        return None, 0

    def articles(self):
        from lib.models.article import Article
        sql = "SELECT id, title, author_id, magazine_id FROM articles WHERE author_id = %s;"
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Article.instance_from_db(row) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine
        CURSOR.execute("""
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazine m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = %s
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        CURSOR.execute("""
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = %s
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [row[0] for row in rows]
