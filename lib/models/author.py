from ..db.connection import CURSOR, CONN


class Author:
   all = {}
  
   def __init__(self,name,id = None):
       self.id = id
       self.name = name
   def __repr__(self):
       return f"<Author {self.id}: {self.name}>"
   @property
   def name(self):
       return self._name
   @name.setter
   def name(self, value):
       if not isinstance(value,str) or len(value.strip()) == 0:
           raise ValueError("Author name must be a non_empty string.")
       self._name = value.strip()


#    @classmethod
#    def create_table(cls):
#        """Create a new table to persits the attributes of Authorinstances"""


#        sql = """CREATE TABLE IF NOT EXISTS authors(
#                  id SERIAL INTEGER PRIMARY KEY,
#                  name VARCHAR(255) NOT NULL
#                  );
#                  """
#        CURSOR.execute(sql)
#        CONN.commit()


   def save(self):
       sql = """ INSERT INTO authors (name)
       VALUES (?)
       """
       CURSOR.execute(sql, (self.name))
       CONN.commit()


       self.id = CURSOR.lastrowid
       Author.all[self.id] =id


   @classmethod
   def instance_from_db(cls,row):
       author = cls.all.get(row[0])
       if author:
          author.name  =row[1]
       else:
           author = cls(row[1], id = row[0])
           cls.all[author.id] = author
       return author


                              
   @classmethod
   def find_by_id(cls, id):
       sql = """SELECT *
                 FROM authors
                 WHERE id = ?
                 """
      
       row = CURSOR.execute(sql, (id,)).fetchone()
       return cls.instance_from_db(row) if row else None
  
      
   @classmethod
   def find_by_name(cls, name):
       sql = """SELECT *
                FROM authors
                WHERE name is ?
                """
       row = CURSOR.execute(sql, (name,)).fetchone()
       return cls.instace_from_db(row) if row else None
   @classmethod
   def find_all(cls):
       sql = """SELECT *
               FROM authors
               """
       rows = CURSOR.execute(sql).fetchall()


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
        return author, row[2]  # Return author instance and article count
    return None, 0

   def articles(self):
      from lib.models.article import Article
      sql = "SELECT id, title, author_id, magazine_id FROM articles WHERE author_id = %s;"
      CURSOR.execute(sql, (self.id))
      rows = CURSOR.fetchall()
      return [Article.instance_from_db(row) for row in rows]
   def magazines(self):
       CURSOR.execute("""
                         SELECT DISTINCT m.id, m.name, m.category
                      FROM maazine m
                      JOIN articles a ON m.id = a.magazine_id
                      WHERE a.author_id = %s
                      """, (self.id,))
       from lib.models.magazine import Magazine
       rows = CURSOR.fetchall()
       return [Magazine(id = row[0], name = row[1],category = row[2]) for row in rows]
  
   def add_article(self, magazine, title):
        """Create and save a new Article for this author in the given magazine."""
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

   def topic_areas(self):
        """Return unique list of magazine categories (topics) this author has contributed to."""
        CURSOR.execute("""
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = %s
        """, (self.id,))
        rows = CURSOR.fetchall()
        return [row[0] for row in rows]
  





