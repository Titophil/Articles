from ..db.connection import CURSOR, CONN

class Article:
    all = {}

    def __init__(self, id=None,title = None,author_id = None,magazine_id = None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id


    def __repr__(self):
        return f"<Article {self.id}: {self.title}, {self.author_id}, {self.magazine_id}>"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Article name must be a non-empty string.")
        self._title = value.strip()


    # # @classmethod
    # # def create_table(cls):
    # #     """Create a new table to persist Magazine instances"""
    # #     sql = """
    # #     CREATE TABLE IF NOT EXISTS articles (
    # #         id SERIAL PRIMARY KEY,
    # #         title VARCHAR(255) NOT NULL,
    # #         author_id INTEGER,
    # #         magazine_id INTEGER,
    # #         FOREIGN KEY(author_id) REFERENCES authors(id),
    # #         FOREIGN KEY(magazine_id) REFERENCES magazines(id)
      
    # #     );
    # #     """
    #     CURSOR.execute(sql)
    #     CONN.commit()

    def save(self):
        sql = """
        INSERT INTO articles (title, author_id,magazine_id)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        CURSOR.execute(sql, (self.title, self.author_id, self.magazine_id))
        self.id = CURSOR.fetchone()[0]
        CONN.commit()
        Article.all[self.id] = self

    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            article.title = row[1]
            article.author_id = row[2]
            article.magazine_id = row[3]
        else:
            article = cls(id=row[0], title=row[1], author_id=row[2], magazine_id = row[3])
            cls.all[article.id] = article
        return article

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM articles WHERE id = %s;"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        sql = "SELECT * FROM articles WHERE title = %s;"
        CURSOR.execute(sql, (title,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_author(cls, author_id):
        sql = "SELECT * FROM articles WHERE author_id = %s;"
        CURSOR.execute(sql, (author_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    @classmethod
    def find_by_magazine(cls, magazine_id):
        sql = "SELECT * FROM articles WHERE magazine_id = %s;"
        CURSOR.execute(sql, (magazine_id,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def author(self):
        from lib.models.author import Author
        sql = "SELECT id, name FROM authors WHERE id = %s;"
        CURSOR.execute(sql, (self.author_id,))
        row = CURSOR.fetchone()
        return [Author(id=row[0], name = row[1]) if row else None]
    def magazine(self):
        from lib.models.magazine import Magazine
        sql = "SELECT id, name, category FROM magazines WHERE id = %s;"
        CURSOR.execute(sql, (self.magazine_id,))
        row = CURSOR.fetchone()
        return Magazine(id=row[0], name=row[1], category=row[2]) if row else None
