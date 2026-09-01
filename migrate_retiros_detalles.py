import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def run():
    print("Migrating retiros table to add detalles column...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("ALTER TABLE retiros ADD COLUMN IF NOT EXISTS detalles TEXT;")
        conn.commit()
        print("Success!")
    except Exception as e:
        print("Error:", e)
    finally:
        if 'conn' in locals() and conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    run()
