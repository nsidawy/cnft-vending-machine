import psycopg2
import config

def read(query: str):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config.config("postgresql")
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        # display the PostgreSQL database server version
        results = cur.fetchall()
        cur.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
