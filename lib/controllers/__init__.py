
from db.connection import connection, schema, seed
from lib.models import author, article, magazine
from lib.scripts import run_queries

schema() 
seed()