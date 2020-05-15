
import psycopg2
from psycopg2 import Error, extras


class Sql:
    """Model component of MVC architecture"""

    def __init__(self):
        self.user = "blake"
        self.password = "root"
        self.host = "127.0.0.1"
        self.port = 5432
        self.database = "postgres"

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
        for item in self._execute(query, return_results=True):
            yield item
        











# PROGRAMS = {
#         'general': {
#             'id': 'general',
#             'name': 'General',
#             'description': 'Overall program to address stiffness and immobility.',
#             'image-link': 'https://cdn4.vectorstock.com/i/1000x1000/07/68/health-medical-heartbeat-pulse-vector-19810768.jpg',
#             'target-areas': [ 'back', 'legs'],
#             'exercises': [ 'inch-worm', 'couch-stretch']
#         },
#         'back': {
#             'id': 'back',
#             'name': 'Back Pain',
#             'description': 'Targeted program to address acute back pain.',
#             'image-link': 'https://cdn1.vectorstock.com/i/1000x1000/68/90/spine-pain-line-icon-body-and-painful-back-ache-vector-25616890.jpg',
#             'target-areas': [ 'back'],
#             'exercises': [ 'inch-worm']
#         }
# }
# 
# EXERCISES = {
#         'inch-worm': {
#             'id': 'inch-worm',
#             'name': 'Inch Worm',
#             'description': 'Key pillar of the Movement Alphabet',
#             'image-link': 'https://img.icons8.com/carbon-copy/2x/exercise.png',
#             'video-link': 'https://www.youtube.com/embed/k3Zi5AYbYU4',
#             'target-areas': [ 'back', 'legs'],
#             'watch-out-for': [ 'Straight Arms', 'Straight Knees', 'Heels On Floor']
#         },
#         'couch-stretch': {
#             'id': 'couch-stretch',
#             'name': 'Couch Stretch',
#             'description': 'Key pillar of the Movement Alphabet',
#             'image-link': 'https://img.icons8.com/carbon-copy/2x/exercise.png',
#             'video-link': 'https://www.youtube.com/embed/hcW3amvueM8',
#             'target-areas': [ 'back', 'legs'],
#             'watch-out-for': [ 'Upright Torso', 'Relaxed Shoulders', 'Heels On Floor']
#         }
# }

