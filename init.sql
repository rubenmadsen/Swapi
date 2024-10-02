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