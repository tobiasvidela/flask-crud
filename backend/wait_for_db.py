import time, psycopg2, os

DB_URL = os.getenv("DB_URL")

while True:
  try:
    conn = psycopg2.connect(DB_URL)
    conn.close()
    print("Database is ready!")
    break
  except psycopg2.OperationalError:
    print("Waiting for database...")
    time.sleep(2)