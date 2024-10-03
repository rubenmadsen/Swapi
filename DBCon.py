import psycopg2
from datetime import datetime
import requests
import json
import pandas as pd
import MRClean
from psycopg2 import sql
from sqlalchemy import create_engine


class DBCon:
    def __init__(self):
        self.con = None
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

        rs = []

        self.add_to_postgres(table_name, json_data)

        for k, v in children.items():
            for url in v:
                self.fetch(k, url)



    def add_to_postgres(self, table_name, json_data):
        if self.exists(table_name, json_data['url']):
            return

        df = MRClean.clean(table_name, json_data)
        #df = pd.DataFrame([json_data])
        engine = create_engine('postgresql+psycopg2://', creator=lambda: self.con)
        if "homeworld" in json_data:
            if not self.exists("planets",json_data['homeworld']) and json_data['homeworld'] is not None:
                self.fetch("planets", json_data['homeworld'])

        existing_df = pd.read_sql(f"SELECT * FROM {table_name} WHERE url = '{json_data['url']}'", con=engine)

        if not existing_df.empty:
            # Compare 'edited' column to decide whether to update the existing record
            existing_edited = existing_df['edited'].iloc[0]
            new_edited = df['edited'].iloc[0]

            if pd.to_datetime(new_edited) > pd.to_datetime(existing_edited):
                # If the new data is more recent, delete the old record and insert the new one
                with engine.connect() as conn:
                    conn.execute(f"DELETE FROM {table_name} WHERE url = '{json_data['url']}'")
                    df.to_sql(table_name, con=engine, if_exists='append', index=False)
        else:
            # If the record doesn't exist, insert it
            df.to_sql(table_name, con=engine, if_exists='append', index=False)

    def create_fact_table(self):
        pass




    def get_characters_and_homeworlds(self):
        try:
            query = """
                SELECT
                    characters.name AS character_name,
                    planets.name AS homeworld_name
                FROM
                    characters
                JOIN
                    planets ON characters.homeworld = planets.url
                ORDER BY
                    characters.name;
            """

            df = pd.read_sql(query, self.con)

            print(df)
            return df

        except Exception as e:
            print(f"An error occurred while retrieving pilots and their homeworlds: {e}")


    # def get_characters_and_homeworlds(self):
    #     try:
    #         with self.con.cursor() as cursor:
    #             cursor.execute("""
    #                 SELECT
    #                     characters.name AS character_name,
    #                     planets.name AS homeworld_name
    #                 FROM
    #                     characters
    #                 JOIN
    #                     planets ON characters.homeworld = planets.url
    #                 ORDER BY
    #                     characters.name;
    #             """)
    #             results = cursor.fetchall()
    #             return results
    #             for row in results:
    #                 character_name, homeworld_name = row
    #                 print(f"Character: {character_name}, Homeworld: {homeworld_name}")
    #     except Exception as e:
    #         print(f"An error occurred while retrieving pilots and their homeworlds: {e}")