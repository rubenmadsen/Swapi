import psycopg2
from datetime import datetime
import requests
import json

class DBCon:
    def __init__(self):
        self.con = None

    def convert_timestamp(self, ts):
        if isinstance(ts, str):
            for fmt in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
                try:
                    return datetime.strptime(ts, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Time data '{ts}' does not match any known format")
        return ts

    def open(self, password):
        try:
            self.con = psycopg2.connect(
                host="localhost",
                port=5432,
                database="postgres",
                user="postgres",
                password=f"{password}"
            )
            # Perform your database operations here
            # Example: cursor.execute("INSERT INTO table_name (column1) VALUES (value1);")

        except Exception as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.con.close()

    def update_starship(self, starship_json):
        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                starship_json['created'] = datetime.strptime(starship_json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                starship_json['edited'] = datetime.strptime(starship_json['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

                values = (
                    starship_json['url'],
                    starship_json['name'],
                    starship_json['model'],
                    starship_json['manufacturer'],
                    starship_json['cost_in_credits'],
                    starship_json['length'],
                    starship_json['max_atmosphering_speed'],
                    starship_json['crew'],
                    starship_json['passengers'],
                    starship_json['cargo_capacity'],
                    starship_json['consumables'],
                    starship_json['hyperdrive_rating'],
                    starship_json['MGLT'],
                    starship_json['starship_class'],
                    starship_json['created'],
                    starship_json['edited']
                )

                cursor.execute("""
                        INSERT INTO starships (
                            url, name, model, manufacturer, cost_in_credits, length,
                            max_atmosphering_speed, crew, passengers, cargo_capacity,
                            consumables, hyperdrive_rating, MGLT, starship_class, created, edited
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (url) DO UPDATE SET
                            name = EXCLUDED.name,
                            model = EXCLUDED.model,
                            manufacturer = EXCLUDED.manufacturer,
                            cost_in_credits = EXCLUDED.cost_in_credits,
                            length = EXCLUDED.length,
                            max_atmosphering_speed = EXCLUDED.max_atmosphering_speed,
                            crew = EXCLUDED.crew,
                            passengers = EXCLUDED.passengers,
                            cargo_capacity = EXCLUDED.cargo_capacity,
                            consumables = EXCLUDED.consumables,
                            hyperdrive_rating = EXCLUDED.hyperdrive_rating,
                            MGLT = EXCLUDED.MGLT,
                            starship_class = EXCLUDED.starship_class,
                            created = EXCLUDED.created,
                            edited = EXCLUDED.edited
                    """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating starship: {e}")
            self.con.rollback()

    def update_character(self, character_json):
        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                character_json['created'] = datetime.strptime(character_json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                character_json['edited'] = datetime.strptime(character_json['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

                # Check if 'homeworld' exists
                homeworld_url = character_json.get('homeworld')
                if homeworld_url:
                    # Check if the homeworld exists in the 'planets' table
                    cursor.execute("SELECT 1 FROM planets WHERE url = %s", (homeworld_url,))
                    if cursor.fetchone() is None:
                        # The planet does not exist in the database, fetch and insert it
                        #planet_data = self.fetch_planet_data(homeworld_url)
                        response = requests.get(homeworld_url)
                        planet_data = json.loads(response.text)
                        if planet_data:
                            self.update_planet(planet_data)
                        else:
                            print(f"Failed to fetch planet data for {homeworld_url}")
                            # Handle the case where planet data couldn't be fetched
                            homeworld_url = None
                else:
                    # If homeworld is None or empty, set to None
                    homeworld_url = None

                # Prepare the values
                values = (
                    character_json['url'],
                    character_json['name'],
                    character_json['height'],
                    character_json['mass'],
                    character_json['hair_color'],
                    character_json['skin_color'],
                    character_json['eye_color'],
                    character_json['birth_year'],
                    character_json['gender'],
                    homeworld_url,
                    character_json['created'],
                    character_json['edited']
                )

                cursor.execute("""
                    INSERT INTO characters (
                        url, name, height, mass, hair_color, skin_color, eye_color,
                        birth_year, gender, homeworld, created, edited
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        name = EXCLUDED.name,
                        height = EXCLUDED.height,
                        mass = EXCLUDED.mass,
                        hair_color = EXCLUDED.hair_color,
                        skin_color = EXCLUDED.skin_color,
                        eye_color = EXCLUDED.eye_color,
                        birth_year = EXCLUDED.birth_year,
                        gender = EXCLUDED.gender,
                        homeworld = EXCLUDED.homeworld,
                        created = EXCLUDED.created,
                        edited = EXCLUDED.edited
                """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating character: {e}")
            self.con.rollback()

    def update_vehicle(self, vehicle_json):


        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                vehicle_json['created'] = self.convert_timestamp(vehicle_json['created'])
                vehicle_json['edited'] = self.convert_timestamp(vehicle_json['edited'])

                values = (
                    vehicle_json['url'],
                    vehicle_json['name'],
                    vehicle_json['model'],
                    vehicle_json['manufacturer'],
                    vehicle_json['cost_in_credits'],
                    vehicle_json['length'],
                    vehicle_json['max_atmosphering_speed'],
                    vehicle_json['crew'],
                    vehicle_json['passengers'],
                    vehicle_json['cargo_capacity'],
                    vehicle_json['consumables'],
                    vehicle_json['vehicle_class'],
                    vehicle_json['created'],
                    vehicle_json['edited']
                )

                cursor.execute("""
                    INSERT INTO vehicles (
                        url, name, model, manufacturer, cost_in_credits, length,
                        max_atmosphering_speed, crew, passengers, cargo_capacity,
                        consumables, vehicle_class, created, edited
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        name = EXCLUDED.name,
                        model = EXCLUDED.model,
                        manufacturer = EXCLUDED.manufacturer,
                        cost_in_credits = EXCLUDED.cost_in_credits,
                        length = EXCLUDED.length,
                        max_atmosphering_speed = EXCLUDED.max_atmosphering_speed,
                        crew = EXCLUDED.crew,
                        passengers = EXCLUDED.passengers,
                        cargo_capacity = EXCLUDED.cargo_capacity,
                        consumables = EXCLUDED.consumables,
                        vehicle_class = EXCLUDED.vehicle_class,
                        created = EXCLUDED.created,
                        edited = EXCLUDED.edited
                """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating vehicle: {e}")
            self.con.rollback()

    def update_film(self, film_json):
        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                film_json['created'] = datetime.strptime(film_json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                film_json['edited'] = datetime.strptime(film_json['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')
                film_json['release_date'] = datetime.strptime(film_json['release_date'], '%Y-%m-%d').date()

                values = (
                    film_json['url'],
                    film_json['title'],
                    film_json['episode_id'],
                    film_json['opening_crawl'],
                    film_json['director'],
                    film_json['producer'],
                    film_json['release_date'],
                    film_json['created'],
                    film_json['edited']
                )

                cursor.execute("""
                    INSERT INTO films (
                        url, title, episode_id, opening_crawl, director, producer,
                        release_date, created, edited
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        title = EXCLUDED.title,
                        episode_id = EXCLUDED.episode_id,
                        opening_crawl = EXCLUDED.opening_crawl,
                        director = EXCLUDED.director,
                        producer = EXCLUDED.producer,
                        release_date = EXCLUDED.release_date,
                        created = EXCLUDED.created,
                        edited = EXCLUDED.edited
                """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating film: {e}")
            self.con.rollback()

    def update_planet(self, planet_json):
        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                planet_json['created'] = self.convert_timestamp(planet_json['created'])
                planet_json['edited'] = self.convert_timestamp(planet_json['edited'])
                #planet_json['created'] = datetime.strptime(planet_json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                #planet_json['edited'] = datetime.strptime(planet_json['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

                values = (
                    planet_json['url'],
                    planet_json['name'],
                    planet_json['rotation_period'],
                    planet_json['orbital_period'],
                    planet_json['diameter'],
                    planet_json['climate'],
                    planet_json['gravity'],
                    planet_json['terrain'],
                    planet_json['surface_water'],
                    planet_json['population'],
                    planet_json['created'],
                    planet_json['edited']
                )

                cursor.execute("""
                    INSERT INTO planets (
                        url, name, rotation_period, orbital_period, diameter, climate,
                        gravity, terrain, surface_water, population, created, edited
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        name = EXCLUDED.name,
                        rotation_period = EXCLUDED.rotation_period,
                        orbital_period = EXCLUDED.orbital_period,
                        diameter = EXCLUDED.diameter,
                        climate = EXCLUDED.climate,
                        gravity = EXCLUDED.gravity,
                        terrain = EXCLUDED.terrain,
                        surface_water = EXCLUDED.surface_water,
                        population = EXCLUDED.population,
                        created = EXCLUDED.created,
                        edited = EXCLUDED.edited
                """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating planet: {e}")
            self.con.rollback()

    def update_species(self, species_json):
        try:
            with self.con.cursor() as cursor:
                # Parse datetime fields
                species_json['created'] = datetime.strptime(species_json['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                species_json['edited'] = datetime.strptime(species_json['edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

                # Check if 'homeworld' is not None or empty
                homeworld_url = species_json.get('homeworld')
                if homeworld_url:
                    # Check if the homeworld exists in the 'planets' table
                    cursor.execute("SELECT 1 FROM planets WHERE url = %s", (homeworld_url,))
                    if cursor.fetchone() is None:
                        # The planet does not exist in the database, fetch and insert it
                        #planet_data = self.fetch_planet_data(homeworld_url)
                        response = requests.get(homeworld_url)
                        planet_data = json.loads(response.text)
                        if planet_data:
                            self.update_planet(planet_data)
                        else:
                            print(f"Failed to fetch planet data for {homeworld_url}")
                            # Handle the case where planet data couldn't be fetched
                            # You might decide to set homeworld to None or skip inserting this species
                            # For this example, let's set homeworld_url to None
                            homeworld_url = None
                else:
                    # If homeworld is None or empty, set to None
                    homeworld_url = None

                # Prepare the values for insertion
                values = (
                    species_json['url'],
                    species_json['name'],
                    species_json['classification'],
                    species_json['designation'],
                    species_json['average_height'],
                    species_json['skin_colors'],
                    species_json['hair_colors'],
                    species_json['eye_colors'],
                    species_json['average_lifespan'],
                    homeworld_url,
                    species_json['language'],
                    species_json['created'],
                    species_json['edited']
                )

                cursor.execute("""
                    INSERT INTO species (
                        url, name, classification, designation, average_height,
                        skin_colors, hair_colors, eye_colors, average_lifespan,
                        homeworld, language, created, edited
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO UPDATE SET
                        name = EXCLUDED.name,
                        classification = EXCLUDED.classification,
                        designation = EXCLUDED.designation,
                        average_height = EXCLUDED.average_height,
                        skin_colors = EXCLUDED.skin_colors,
                        hair_colors = EXCLUDED.hair_colors,
                        eye_colors = EXCLUDED.eye_colors,
                        average_lifespan = EXCLUDED.average_lifespan,
                        homeworld = EXCLUDED.homeworld,
                        language = EXCLUDED.language,
                        created = EXCLUDED.created,
                        edited = EXCLUDED.edited
                """, values)
                self.con.commit()
        except Exception as e:
            print(f"An error occurred while inserting/updating species: {e}")
            self.con.rollback()
