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
