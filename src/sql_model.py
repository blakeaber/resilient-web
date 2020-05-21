
import psycopg2
from psycopg2 import Error, extras


class Sql:
    """Model component of MVC architecture"""

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def _commit_records(self, conn, query):
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

    def _return_records(self, conn, query):
        with conn.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                yield row  

    def _execute(self, query, return_results=False):
        conn = None

        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                cursor_factory=extras.DictCursor
            )

            if return_results:
                for item in self._return_records(conn, query):
                    yield item
            else:
                self._commit_records(conn, query)
                
        except (Exception, psycopg2.DatabaseError) as error:
            print ("Error while creating PostgreSQL table:", error)

        finally:
            if conn:
                conn.close()
    
    def select(self, query):
        return self._execute(query, return_results=True)

    def insert(self, query):
        return self._execute(query, return_results=False)

