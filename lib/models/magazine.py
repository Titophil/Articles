from ..db.connection import CURSOR, CONN

class Magazine:
    all = {}

    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name}, {self.category}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Magazine name must be a non-empty string.")
        self._name = value.strip()

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, value):
        if not isinstance(value,str) or len(value.strip()) == 0:
            raise ValueError("Magazine category must be a non-empty string.")
        self._category = value.strip()

    # @classmethod
    # def create_table(cls):
    #     """Create a new table to persist Magazine instances"""
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS magazines (
    #         id SERIAL PRIMARY KEY,
    #         name VARCHAR(255) NOT NULL,
    #         category VARCHAR(255) NOT NULL
    #     );
    #     """
    #     CURSOR.execute(sql)
    #     CONN.commit()

    def save(self):
        sql = """
        INSERT INTO magazines (name, category)
        VALUES (%s, %s)
        RETURNING id;
        """
        CURSOR.execute(sql, (self.name, self.category))
        self.id = CURSOR.fetchone()[0]
        CONN.commit()
        Magazine.all[self.id] = self

    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(id=row[0], name=row[1], category=row[2])
            cls.all[magazine.id] = magazine
        return magazine

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM magazines WHERE id = %s;"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM magazines WHERE name = %s;"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_category(cls, category):
        sql = "SELECT * FROM magazines WHERE category = %s;"
        CURSOR.execute(sql, (category,))
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
    @classmethod
    def magazines_with_multiple_authors(cls):
        CURSOR.execute("""SELECT m.id, n.name, m.category
                       FROM magazines m
                       JOIN articles a ON m.id = a.magazine_id
                       GROUP BY m.id
                       HAVING COUNT(DISTINCT a.author_id >=2;
                       )""")
        rows = CURSOR.fetchall()
        return [cls(id = row[0], name = row[1], category = row[2]) for row in rows]

    @classmethod
    def article_counts(cls):
       CURSOR.execute("""
        SELECT m.id, m.name, m.category, COUNT(a.id) AS article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id;
    """)
       rows = CURSOR.fetchall()
       return [(cls(id=row[0], name=row[1], category=row[2]), row[3]) for row in rows]


    def articles(self):
        from lib.models.article import Article
        sql = "SELECT id, title, author_id, magazine_id FROM articles WHERE magazine_id = %s;"
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def authors(self):
        from lib.models.author import Author
        sql = """
        SELECT DISTINCT a.id, a.name
        FROM authors a
        JOIN articles ar ON a.id = ar.author_id
        WHERE ar.magazine_id = %s;
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(id=row[0], name=row[1]) for row in rows]
    def contributors(self):
        """Return unique list of Author instances who have written for this magazine."""
        CURSOR.execute("""
            SELECT DISTINCT au.id, au.name
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = %s
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(id=row[0], name=row[1]) for row in rows]

    def article_titles(self):
        """Return list of titles of all articles in this magazine."""
        CURSOR.execute("""
            SELECT title
            FROM articles
            WHERE magazine_id = %s
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [row[0] for row in rows]

    def contributing_authors(self):
        """
        Return list of Author instances who have written more than 2 articles 
        in this magazine.
        """
        CURSOR.execute("""
            SELECT au.id, au.name
            FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = %s
            GROUP BY au.id, au.name
            HAVING COUNT(a.id) > 2
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(id=row[0], name=row[1]) for row in rows]
