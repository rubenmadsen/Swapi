CREATE TABLE films (
    url TEXT PRIMARY KEY,
    title TEXT,
    episode_id INTEGER,
    opening_crawl TEXT,
    director TEXT,
    producer TEXT,
    release_date DATE,
    created TIMESTAMP,
    edited TIMESTAMP
);

CREATE TABLE planets (
    url TEXT PRIMARY KEY,
    name TEXT,
    rotation_period INTEGER,
    orbital_period INTEGER,
    diameter INTEGER,
    climate TEXT,
    gravity NUMERIC,
    terrain TEXT,
    surface_water NUMERIC,
    population BIGINT,
    created TIMESTAMP,
    edited TIMESTAMP
);

CREATE TABLE characters (
    url TEXT PRIMARY KEY,
    name TEXT,
    height INTEGER,
    mass INTEGER,
    hair_color TEXT,
    skin_color TEXT,
    eye_color TEXT,
    birth_year TEXT,
    gender TEXT,
    homeworld TEXT REFERENCES planets(url),
    created TIMESTAMP,
    edited TIMESTAMP
);



CREATE TABLE starships (
    url TEXT PRIMARY KEY,
    name TEXT,
    model TEXT,
    manufacturer TEXT,
    cost_in_credits BIGINT,
    length NUMERIC,
    max_atmosphering_speed INTEGER,
    crew INTEGER,
    passengers INTEGER,
    cargo_capacity BIGINT,
    consumables TEXT,
    hyperdrive_rating NUMERIC,
    "MGLT" INTEGER,
    starship_class TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);

CREATE TABLE vehicles (
    url TEXT PRIMARY KEY,
    name TEXT,
    model TEXT,
    manufacturer TEXT,
    cost_in_credits BIGINT,
    length NUMERIC,
    max_atmosphering_speed INTEGER,
    crew INTEGER,
    passengers INTEGER,
    cargo_capacity BIGINT,
    consumables TEXT,
    vehicle_class TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);
CREATE TABLE species (
    url TEXT PRIMARY KEY,
    name TEXT,
    classification TEXT,
    designation TEXT,
    average_height INTEGER,
    skin_colors TEXT,
    hair_colors TEXT,
    eye_colors TEXT,
    average_lifespan INTEGER,
    homeworld TEXT REFERENCES planets(url),
    language TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);




CREATE TABLE films_characters (
    films_url TEXT REFERENCES films(url) ON DELETE NO ACTION,
    characters_url TEXT REFERENCES characters(url) ON DELETE NO ACTION,
    PRIMARY KEY (films_url, characters_url)
);

CREATE TABLE films_starships (
    films_url TEXT REFERENCES films(url) ON DELETE NO ACTION,
    starships_url TEXT REFERENCES starships(url) ON DELETE NO ACTION,
    PRIMARY KEY (films_url, starships_url)
);

CREATE TABLE films_planets (
    films_url TEXT REFERENCES films(url) ON DELETE NO ACTION,
    planets_url TEXT REFERENCES planets(url) ON DELETE NO ACTION,
    PRIMARY KEY (films_url, planets_url)
);

CREATE TABLE films_vehicles (
    films_url TEXT REFERENCES films(url) ON DELETE NO ACTION,
    vehicles_url TEXT REFERENCES vehicles(url) ON DELETE NO ACTION,
    PRIMARY KEY (films_url, vehicles_url)
);

CREATE TABLE films_species (
    films_url TEXT REFERENCES films(url) ON DELETE NO ACTION,
    species_url TEXT REFERENCES species(url) ON DELETE NO ACTION,
    PRIMARY KEY (films_url, species_url)
);

CREATE TABLE characters_starships (
    characters_url TEXT REFERENCES characters(url) ON DELETE NO ACTION,
    starships_url TEXT REFERENCES starships(url) ON DELETE NO ACTION,
    PRIMARY KEY (characters_url, starships_url)
);

CREATE TABLE characters_vehicles (
    characters_url TEXT REFERENCES characters(url) ON DELETE NO ACTION,
    vehicles_url TEXT REFERENCES vehicles(url) ON DELETE NO ACTION,
    PRIMARY KEY (characters_url, vehicles_url)
);

CREATE TABLE characters_planets (
    characters_url TEXT REFERENCES characters(url) ON DELETE NO ACTION,
    planets_url TEXT REFERENCES planets(url) ON DELETE NO ACTION,
    PRIMARY KEY (characters_url, planets_url)
);
CREATE TABLE characters_species (
    characters_url TEXT REFERENCES characters(url) ON DELETE NO ACTION,
    species_url TEXT REFERENCES species(url) ON DELETE NO ACTION,
    PRIMARY KEY (characters_url, species_url)
);
