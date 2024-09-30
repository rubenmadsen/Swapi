import os
import pprint
from DBCon import DBCon
pp = pprint.PrettyPrinter(indent=2, width=80, compact=False)

import requests
import json

url = "https://swapi.dev/api/"
db = DBCon()

urls = {
    "films": set(),
    "planets": set(),
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


def pull_urls(film):
    try:
        for k, v in film.items():
            if isinstance(v, list):
                urls[k].update(v)

    except Exception as e:
        print(f"Error: {e}")


def store_url(label, fn):
    for lable_url in urls[label]:
        response = requests.get(lable_url)
        #print(response.status_code)
        data = json.loads(response.text)
        fn(data) #db.update_starship(data)


def run():
    db.open(pw)
    print("Database opened")

    for film in urls["films"]:
        response = requests.get(film)
        #print(response.status_code)
        pull_urls(json.loads(response.text))
    #pp.pprint(urls)
    print("Planets")
    store_url("planets", db.update_planet)
    print("Starships")
    store_url("starships",db.update_starship)
    print("Characters")
    store_url("characters", db.update_character)
    print("Species")
    store_url("species", db.update_species)
    print("Vehicles")
    store_url("vehicles", db.update_vehicle)
    print("Films")
    store_url("films", db.update_film)

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