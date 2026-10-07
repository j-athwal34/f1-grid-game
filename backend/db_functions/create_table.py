import os, psycopg
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL_POOLED") # fetching the credentials from .env file

with psycopg.connect(url) as conn: # opens the connection
    with conn.cursor() as cur: # opens the cursor to which SQL is powered through
        cur.execute("CREATE TABLE IF NOT EXISTS stats( id INT PRIMARY KEY, total_games INT NOT NULL DEFAULT 0); ") 

        cur.execute("INSERT INTO stats (id, total_games) VALUES (1, 0) ON CONFLICT (id) DO NOTHING;")
        cur.execute("SELECT total_games FROM stats WHERE id=1;")

        print("Table ready, games played: ", cur.fetchone()[0])