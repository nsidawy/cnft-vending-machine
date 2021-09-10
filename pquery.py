import psycopg2 #type: ignore
import config

def read(query: str):
    conn = None
    try:
        params = config.config("postgresql")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def write(query: str):
    conn = None
    try:
        params = config.config("postgresql")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
