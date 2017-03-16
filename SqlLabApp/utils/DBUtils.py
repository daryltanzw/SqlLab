import psycopg2

DBNAME = "sqllabdb"
HOST = "localhost"
USERNAME = "postgres"
PASSWORD = "postgres"


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(DBNAME, USERNAME, HOST, PASSWORD))
    except:
        print "Unable to connect do DB"

    return conn
