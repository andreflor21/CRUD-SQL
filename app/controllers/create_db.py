import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

load_dotenv()
configs = {
    "host": os.environ.get('DB_HOST'),
    "database": os.environ.get('DB_NAME'),
    "user": os.environ.get('DB_USER'),
    "password": os.environ.get('DB_PWD')
}

def create_db():
    conn = psycopg2.connect(user=configs['user'], password=configs['password'])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    database = os.environ.get('DB_NAME')

    try: 
        cur.execute('CREATE DATABASE %s' % database )
    except psycopg2.DatabaseError: 
        pass

    cur.close()
    conn.close()

def create_table():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS animes (
            id              BIGSERIAL PRIMARY KEY,
            anime           VARCHAR(100) NOT NULL UNIQUE,
            released_date   DATE NOT NULL,
            seasons         INTEGER NOT NULL
        );
    """

    cur.execute(query=query)
    conn.commit()
    cur.close()
    conn.close()