import psycopg2
from config.settings import DATABASES

class DAOService:

    def __init__(self):
        self.conn = self.create_db_client()

    def create_db_client(self):
        db_config = DATABASES['default']
        conn = psycopg2.connect(
            host=db_config['HOST'],
            database=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            port=db_config['PORT']
        )
        return conn

    def findBook(self, title):
        query = "SELECT * FROM books WHERE UPPER(title) = UPPER(%s)"
        params = (title,)
        return self.read(query, params)

    def read(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
        return results

    def insert(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    def close(self):
        self.conn.close()