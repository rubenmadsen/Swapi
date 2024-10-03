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
    gravity TEXT,
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
    film_url TEXT REFERENCES films(url) ON DELETE CASCADE,
    character_url TEXT REFERENCES characters(url) ON DELETE CASCADE,
    PRIMARY KEY (film_url, character_url)
);

CREATE TABLE films_starships (
    film_url TEXT REFERENCES films(url) ON DELETE CASCADE,
    starship_url TEXT REFERENCES starships(url) ON DELETE CASCADE,
    PRIMARY KEY (film_url, starship_url)
);

CREATE TABLE films_planets (
    film_url TEXT REFERENCES films(url) ON DELETE CASCADE,
    planet_url TEXT REFERENCES planets(url) ON DELETE CASCADE,
    PRIMARY KEY (film_url, planet_url)
);

CREATE TABLE films_vehicles (
    film_url TEXT REFERENCES films(url) ON DELETE CASCADE,
    vehicle_url TEXT REFERENCES vehicles(url) ON DELETE CASCADE,
    PRIMARY KEY (film_url, vehicle_url)
);

CREATE TABLE films_species (
    film_url TEXT REFERENCES films(url) ON DELETE CASCADE,
    species_url TEXT REFERENCES species(url) ON DELETE CASCADE,
    PRIMARY KEY (film_url, species_url)
);

CREATE TABLE characters_starships (
    character_url TEXT REFERENCES characters(url) ON DELETE CASCADE,
    starship_url TEXT REFERENCES starships(url) ON DELETE CASCADE,
    PRIMARY KEY (character_url, starship_url)
);

CREATE TABLE characters_vehicles (
    character_url TEXT REFERENCES characters(url) ON DELETE CASCADE,
    vehicle_url TEXT REFERENCES vehicles(url) ON DELETE CASCADE,
    PRIMARY KEY (character_url, vehicle_url)
);





