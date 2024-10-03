import pandas as pd
from datetime import datetime

def convert_timestamp(ts):
    if isinstance(ts, str):
        for fmt in ('%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'):
            try:
                return datetime.strptime(ts, fmt)
            except ValueError:
                continue
        raise ValueError(f"Time data '{ts}' does not match any known format")
    return ts

def clean_starship(df):
    def process_crew_value(value):
        if isinstance(value, str) and '-' in value:
            lower, upper = map(int, value.split('-'))
            return (lower + upper) // 2
        elif isinstance(value, str):
            return int(value.replace(",", ""))
        else:
            return 0

    df["crew"] = df["crew"].apply(process_crew_value)
    df["max_atmosphering_speed"] = pd.to_numeric(df["max_atmosphering_speed"].str.extract(r'(\d+)')[0],
                                                 errors='coerce').fillna(0).astype(int)
    df["passengers"] = pd.to_numeric(df["passengers"].str.replace(",", ""), errors='coerce').fillna(0).astype(int)
    df["length"] = pd.to_numeric(df["length"].str.extract(r'(\d+\.?\d*)')[0], errors='coerce')


def clean_character(df):
    df["mass"] = pd.to_numeric(df["mass"].str.replace(",", ""), errors='coerce').fillna(0).astype(int)

def clean_species(df):
    pass
def clean(table_name, json_data):
    json_data['edited'] = convert_timestamp(json_data["edited"])
    json_data['created'] = convert_timestamp(json_data["created"])
    deletion = list()
    for k, v in json_data.items():
        if isinstance(v, list):
            json_data[k] = ','.join(v)
            deletion.append(k)
        if v == "unknown" or v == "NaN" or v == "n/a" or v == "none" or v == "indefinite":
            json_data[k] = None

    for d in deletion:
        del json_data[d]

    df = pd.DataFrame([json_data])

    if table_name == "starships":
        clean_starship(df)
    elif table_name == "characters":
        clean_character(df)

    return df
