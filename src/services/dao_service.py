import psycopg2
from typing import List, Dict, Any
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
                (p.embedding <=> embedding('textembedding-gecko@003', %s)::vector) AS distance
            FROM
                pages p
            JOIN books b ON
                p.book_id = b.book_id
            JOIN authors a ON
                a.author_id = b.author_id
        """

        parameters = [str(characterLimit), prompt, book, author]
        print(f"Parameters: {parameters}")
        params = [p for p in parameters if p is not None and (isinstance(p, str) and p != '')]

        print(f"Parameters: {params}")

        if len(params) > 2:
            sql += self.create_where_clause(book, author)

        sql += """
            ORDER BY
                distance ASC
            LIMIT 10;
        """

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

    def create_where_clause(self, book: str, author: str) -> str:
        """
        Creates a WHERE clause for the SQL query based on book and author filters.

        Args:
            book (str): The book title to filter by.
            author (str): The author to filter by.

        Returns:
            str: The WHERE clause for the SQL query.
        """
        where_clause = " WHERE "
        conditions = []
        if book:
            conditions.append(f"b.title = %s")
        if author:
            conditions.append(f"a.name = %s")
        where_clause += " AND ".join(conditions)
        return where_clause

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