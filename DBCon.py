import psycopg2
from datetime import datetime
import requests
import json
import pandas as pd
from psycopg2 import sql
from sqlalchemy import create_engine


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

    def add_to_postgres(self, table_name, data_json):
        df = pd.DataFrame([data_json])
        engine = create_engine('postgresql+psycopg2://', creator=lambda:self.con)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)


    def get_characters_and_homeworlds(self):
        try:
            with self.con.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        characters.name AS character_name,
                        planets.name AS homeworld_name
                    FROM
                        characters
                    JOIN
                        planets ON characters.homeworld = planets.url
                    ORDER BY
                        characters.name;
                """)
                results = cursor.fetchall()
                return results
                for row in results:
                    character_name, homeworld_name = row
                    print(f"Character: {character_name}, Homeworld: {homeworld_name}")
        except Exception as e:
            print(f"An error occurred while retrieving pilots and their homeworlds: {e}")