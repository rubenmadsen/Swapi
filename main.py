import os

import requests
import psycopg2
import json

url = "https://swapi.dev/api/"
db = None
films = set()
planets = set()
spaceships = set()
vehicles = set()
people = set()
species = set()

films.add(f"{url}films/1/")
films.add(f"{url}films/2/")
films.add(f"{url}films/3/")
films.add(f"{url}films/4/")
films.add(f"{url}films/5/")
films.add(f"{url}films/6/")

def parse_film(film):
    parent = ''
    keys = set()
    json_data = {}
    if isinstance(parent, str):
        for k, v in film.items():
            #full_key = k #f"{parent}.{k}" if parent else k
            keys.add(k)
            json_data[k] = v
        if isinstance(parent, list):
        print(f"Dolk")
    print(f"Data: {json_data}")

def pull_data():
    for film in films:
        response = requests.get(film)
        print(response.status_code)
        parse_film(json.loads(response.text))
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
    pass
    #response = requests.get(f"{people_url}{8}")
    #data = json.loads(response.text)
    #keys = set()
    #parent = ''
    #for k, v in data.items():
        #full_key = f"{parent}.{k}" if parent else k
        #keys.add(full_key)
        #print("Key: " + full_key)


    #print(keys)



if __name__ == "__main__":
    pw = os.environ.get('POSTGRES_PASSWORD')
    open_db(pw)
    pull_data()
    run()
