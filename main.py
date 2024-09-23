import os

import requests
import psycopg2

url = "https://swapi.dev/api/"
people_url = f"{url}people/"
db = None
def open_db(password):
    global db
    try:
        print("Password:" + str(password))
        db = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password=f"{password}"
        )
        cursor = db.cursor()
        # Perform your database operations here
        # Example: cursor.execute("INSERT INTO table_name (column1) VALUES (value1);")
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def run():
    response = requests.get(f"{people_url}{8}")
    print(response.json())



if __name__ == "__main__":
    pw = os.environ.get('POSTGRES_PASSWORD')
    open_db(pw)
    run()
