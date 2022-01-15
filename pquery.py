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
    finally:
        if conn is not None:
            conn.close()

def write_and_get_id(query: str):
    conn = None
    try:
        params = config.config("postgresql")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()

        cur = conn.cursor()
        cur.execute("select lastval();")
        id = cur.fetchall()[0][0]
        cur.close()
        return id
    finally:
        if conn is not None:
            conn.close()
