import psycopg2
from typing import List, Dict, Any
from config.settings import DATABASES

class DAOService:

    def __init__(self):
        self.conn = self.create_db_client()
        db_config = DATABASES['default']
        self.embeddings = db_config['EMBEDDING_MODEL']
        self.cosine_distance = db_config['COSINE_DISTANCE']

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

    def find_book(self, title):
        query = "SELECT * FROM books WHERE UPPER(title) = UPPER(%s)"
        params = (title,)
        return self.read(query, params)
    def prompt_for_books(self, prompt: str, book: str = None, author: str = None, characterLimit: int = None) -> List[Dict[str, Any]]:
        """
        Prompts for books based on a given prompt, book title, and author. Vertexai integration will
        automatically transform prompt to text embeddings

        Args:
            prompt (str): The prompt to use for searching.
            book (str, optional): The book title to filter by. Defaults to None.
            author (str, optional): The author to filter by. Defaults to None.
            characterLimit (int, optional): The maximum number of characters to return for the page content. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the search results.
        """
        if characterLimit is None or characterLimit == 0:
            characterLimit = 2000

        sql = """
            SELECT
                b.title,
                LEFT(p.content, %s) AS page,
                a.name,
                p.page_number,
                (p.embedding <=> embedding(%s, %s)::vector) AS distance
            FROM
                pages p
            JOIN books b ON
                p.book_id = b.book_id
            JOIN authors a ON
                a.author_id = b.author_id
        """

        parameters = [str(characterLimit), self.embeddings, prompt, book, author, self.embeddings, prompt, self.cosine_distance]
        print(f"Parameters: {parameters}")
        params = [p for p in parameters if p is not None and (isinstance(p, str) and p != '')]

        print(f"Parameters: {params}")
        whereClause = """ WHERE """
        if len(params) > 3:
            sql += self.create_where_clause(book, author)
            whereClause = """ AND """
        sql += whereClause
        sql += """(p.embedding <=> embedding(%s, %s)::vector) < %s """

        sql += """ ORDER BY distance ASC LIMIT 10 """

        print(f"SQL: {sql}")

        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        result_rows = []
        for row in rows:
            result_rows.append(dict(zip([desc[0] for desc in cursor.description], row)))
        print(result_rows)
        return result_rows

    def create_where_clause(self, book: str = None, author: str = None) -> str:
        where_clause = " WHERE "
        conditions = []
        if book:  # Check if book is actually provided (after filtering)
            conditions.append(f"b.title = %s")
        if author:  # Check if author is actually provided (after filtering)
            conditions.append(f"a.name = %s")

        # Handle case where no book or author is provided:
        if not conditions:
            return ""  # Or raise an appropriate exception if filtering is required.

        where_clause += " AND ".join(conditions)
        return where_clause
    def find_book(self, title):
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

    def insert_pages(self, book_id: int, content: str, page_number: int) -> int:
        sql = """
            INSERT INTO pages (book_id, content, page_number)
            VALUES (%s, %s, %s);
        """
        params = (book_id, content, page_number)
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            self.conn.commit()
            return cursor.rowcount  # Return the number of rows affected


    def insert_summaries(self, book_id: int, summary: str) -> int:
        sql = """
            INSERT INTO bookSummaries (book_id, summary)
            VALUES (%s, %s);
        """
        params = (book_id, summary)
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            self.conn.commit()
            return cursor.rowcount

    def insert_author(self, bio: str, author: str) -> int:
        sql = """
            INSERT INTO authors (bio, name)
            VALUES (%s, %s)
            RETURNING author_id;
        """
        params = (bio, author)
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            author_id = cursor.fetchone()[0]  # Fetch the returned author_id
            self.conn.commit()
            return author_id

    def insert_book(self, author_id: int, title: str, year: str, public_private: str) -> int: # Use string for scope
        sql = """
            INSERT INTO books (author_id, publication_year, title, scope)
            VALUES (%s, %s, %s, %s)
            RETURNING book_id;
        """
        params = (author_id, year, title, public_private)  # Pass year as string, DB will handle conversion if needed.
        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            book_id = cursor.fetchone()[0]
            self.conn.commit()
            return book_id