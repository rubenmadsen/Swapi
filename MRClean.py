




def clean_starship(df):
    pass


def clean_character(df):
    pass


def clean(table_name, df):
    if table_name == "starships":
        clean_starship(df)
    elif table_name == "characters":
        clean_character(df)
