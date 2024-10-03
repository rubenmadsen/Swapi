import psycopg2
from datetime import datetime
import requests
import json
import pandas as pd
import MRClean
from psycopg2 import sql
from sqlalchemy import create_engine, text



class DBCon:
    def __init__(self):
        self.con = None
        self.relationships = {
            "films" : {
                "key": "key",
                "children": set()
            }
        }


        self.names = {
            'characters': 'characters',
            'films': 'films',
            'species': 'species',
            'planets': 'planets',
            'starships': 'starships',
            'vehicles': 'vehicles',
            'pilots': 'characters',
            'people': 'characters',
            'residents': 'characters'
        }



    def exists(self, table_name, primary_key):
        table_name = self.names[table_name]
        print(f"Does {primary_key} exist in {table_name}",end=" ")
        cursor = self.con.cursor()
        query = f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE url = %s)"
        cursor.execute(query, (primary_key,))
        exists = cursor.fetchone()[0]
        cursor.close()
        if exists:
            print("Yes")
        else:
            print("No")
        return exists

    def open(self, password):
        try:
            self.con = psycopg2.connect(
                host="127.0.0.1",
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

    template = {
        "parent_name": {
            "table_name": "table_name",
            "key": "partner_key"
        },
        "partner": {
            "table_name": "table_name",
            "key": "partner_key"
        }
    }


    def fetch(self, table_name, url):
        if self.exists(table_name, url):
            return
        table_name = self.names[table_name]
        print(f"Fetching data from {url} to {table_name}")
        response = requests.get(url)
        json_data = response.json()
        children = {}

        for k, v in json_data.items():
            if isinstance(v, list):
                children[k] = v


        parent = url
        self.add_to_postgres(table_name, json_data)

        for k, v in children.items():
            for url in v:
                self.fetch(k, url)
                self.add_relationship(table_name, k, parent, url)



    def add_to_postgres(self, table_name, json_data):
        if self.exists(table_name, json_data['url']):
            return

        df = MRClean.clean(table_name, json_data)
        engine = create_engine('postgresql+psycopg2://', creator=lambda: self.con)
        if "homeworld" in json_data:
            if not self.exists("planets",json_data['homeworld']) and json_data['homeworld'] is not None:
                self.fetch("planets", json_data['homeworld'])

        existing_df = pd.read_sql(f"SELECT * FROM {table_name} WHERE url = '{json_data['url']}'", con=engine)

        if not existing_df.empty:
            existing_edited = existing_df['edited'].iloc[0]
            new_edited = df['edited'].iloc[0]

            if pd.to_datetime(new_edited) > pd.to_datetime(existing_edited):
                with engine.connect() as conn:
                    conn.execute(f"DELETE FROM {table_name} WHERE url = '{json_data['url']}'")
                    df.to_sql(table_name, con=engine, if_exists='append', index=False)
        else:
            df.to_sql(table_name, con=engine, if_exists='append', index=False)

    def calculate_relationship_table_name(self, name1, name2, key1, key2):
        print(name1, name2, key1, key2)
        name1 = self.names[name1]
        name2 = self.names[name2]
        table_name = ""

        if name1 == "films":
            table_name = f"films_{name2}"
        elif name2 == "films":
            table_name = f"films_{name1}"
            key1, key2 = key2, key1
        elif name1 == "characters":
            table_name = f"characters_{name2}"
        elif name2 == "characters":
            table_name = f"characters_{name1}"
            key1, key2 = key2, key1
        else:
            print(name1, name2, key1, key2)
        return table_name, key1, key2

    # def add_relationship(self, table1, table2, key1, key2):
    #     table_name, key1, key2 = self.calculate_relationship_table_name(table1, table2, key1, key2)
    #
    #     if not table_name:
    #         print(f"Cannot determine table name for relationship between {table1} and {table2}")
    #         return
    #
    #     left_field = table_name.split("_")[0] + "_url"
    #     right_field = table_name.split("_")[1] + "_url"
    #
    #     # Check if the relationship already exists
    #     engine = create_engine('postgresql+psycopg2://', creator=lambda: self.con)
    #     existing_rel = pd.read_sql(
    #         f"SELECT * FROM {table_name} WHERE {left_field} = '{key1}' AND {right_field} = '{key2}'", con=engine)
    #     if not existing_rel.empty:
    #         print(f"Relationship between {key1} and {key2} already exists.")
    #         return
    #
    #     # Insert new relationship
    #     query = text(f"INSERT INTO {table_name} ({left_field}, {right_field}) VALUES (:left_val, :right_val)")
    #     with engine.connect() as conn:
    #         conn.execute(query, {"left_val": key1, "right_val": key2})
    #     print(f"Relationship added between {key1} and {key2} in {table_name}")
    def add_relationship(self, table1, table2, key1, key2):
        table_name, key1, key2 = self.calculate_relationship_table_name(table1, table2, key1, key2)
        left_field = table_name.split("_")[0] + "_url"
        right_field = table_name.split("_")[1] + "_url"

        query_check = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {left_field} = %s AND {right_field} = %s)"

        cursor = self.con.cursor()
        cursor.execute(query_check, (key1, key2))
        exists = cursor.fetchone()[0]

        if not exists:
            query_insert = f"INSERT INTO {table_name} ({left_field}, {right_field}) VALUES (%s, %s)"
            try:
                cursor.execute(query_insert, (key1, key2))
                print(f"Relationship added between {key1} and {key2} in {table_name}")
            except Exception as e:
                print(f"Error adding relationship: {e}")
        else:
            print(f"Relationship between {key1} and {key2} already exists in {table_name}")

        cursor.close()
    def create_fact_tables(self):
        self.create_fact_table_gravity_effect()



    def create_fact_table_gravity_effect(self):
        # Create an engine using the provided psycopg2 connection
        engine = create_engine('postgresql+psycopg2://', creator=lambda: self.con)

        # Define the SQL query to join the necessary fields from characters and planets tables
        query = '''
        SELECT 
            characters.name AS character_name, 
            characters.height AS character_height, 
            characters.mass AS character_mass,
            planets.name AS homeplanet_name, 
            planets.gravity AS planet_gravity, 
            planets.diameter AS planet_diameter
        FROM 
            characters
        LEFT JOIN 
            planets ON characters.homeworld = planets.url
        WHERE 
            characters.height IS NOT NULL AND characters.mass IS NOT NULL
        ORDER BY 
        planets.name;
        '''

        # Load the data into a pandas DataFrame
        df = pd.read_sql(query, con=engine)

        # Create the fact table in the database
        fact_table_name = 'fact_character_height_mass_gravity'

        # Push the DataFrame to the fact table
        df.to_sql(fact_table_name, con=engine, if_exists='replace', index=False)

        print(f"Fact table '{fact_table_name}' created successfully with {len(df)} records.")

    # Example usage
    # Assuming 'con' is your open psycopg2 connection
    # create_fact_table(con)

