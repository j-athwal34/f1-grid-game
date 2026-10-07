import os, psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL_POOLED")

def increment_games():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE stats SET total_games = total_games + 1 WHERE id = 1 RETURNING total_games;"
            )
            return cur.fetchone()[0]   # the NEW total, after the increment

def get_total_games():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT total_games FROM stats WHERE id = 1;")
            return cur.fetchone()[0]