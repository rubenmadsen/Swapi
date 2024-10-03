from DBCon import DBCon


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




def run():
    db.open(pw)
    print("Database opened")

    for film in urls["films"]:
        db.fetch("films", film)

    db.create_fact_tables()
    db.close()
    print("Database closed")


if __name__ == "__main__":
    pw = "postgres_password"
    run()

