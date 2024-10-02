import os
import pprint
from DBCon import DBCon
pp = pprint.PrettyPrinter(indent=2, width=80, compact=False)

import requests
import json

url = "https://swapi.dev/api/"
db = DBCon()

urls = {
    "films":    set(),
    "planets":  set(),
    "starships": set(),
    "vehicles": set(),
    "characters": set(),
    "species": set()
}

urls["films"].add(f"{url}films/1/")
urls["films"].add(f"{url}films/2/")
urls["films"].add(f"{url}films/3/")
urls["films"].add(f"{url}films/4/")
urls["films"].add(f"{url}films/5/")
urls["films"].add(f"{url}films/6/")

def flatten(data_json):
    deletion = list()
    for k,v in data_json.items():
        if isinstance(v, list):
            data_json[k] = ','.join(v)
            deletion.append(k)
        if v == "unknown" or v == "NaN" or v == "n/a" or v == "none" or v == "indefinite":
            data_json[k] = None


    for d in deletion:
        del data_json[d]

def pull_urls(film):
    try:
        for k, v in film.items():
            if isinstance(v, list):
                urls[k].update(v)

    except Exception as e:
        print(f"Error: {e}")



def store_url(label):
    for label_url in urls[label]:
        response = requests.get(label_url)
        data = response.json()
        flatten(data)
        #print(f"\tresponse_json:{data}")
        try:
            db.add_to_postgres(label, data)
        except Exception as e:
            print("")
            print("")
            print(f"{label_url}: {e}")
            print(f"Error: {e}")
            print("")
            print("")

def run():
    db.open(pw)
    print("Database opened")

    for film in urls["films"]:
        response = requests.get(film)
        pull_urls(json.loads(response.text))

    # print("Fetching Films...")
    # store_url("films")
    # print("Fetching Planets...")
    # store_url("planets")
    # print("Fetching Starships...")
    # store_url("starships")
    # print("Fetching Characters...")
    # store_url("characters")
    print("Fetching Species...")
    store_url("species")
    print("Fetching Vehicles...")
    store_url("vehicles")

    db.close()
    print("Database closed")


if __name__ == "__main__":
    #pw = os.environ.get('POSTGRES_PASSWORD')
    pw = "postgres_password"
    run()


"""
films > planets > starships > vehicles > characters >
characters > films > species > > planets > starships >
"""