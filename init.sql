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
    rotation_period TEXT,
    orbital_period TEXT,
    diameter TEXT,
    climate TEXT,
    gravity TEXT,
    terrain TEXT,
    surface_water TEXT,
    population TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);

CREATE TABLE characters (
    url TEXT PRIMARY KEY,
    name TEXT,
    height TEXT,
    mass TEXT,
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
    cost_in_credits TEXT,
    length TEXT,
    max_atmosphering_speed TEXT,
    crew TEXT,
    passengers TEXT,
    cargo_capacity TEXT,
    consumables TEXT,
    hyperdrive_rating TEXT,
    MGLT TEXT,
    starship_class TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);

CREATE TABLE vehicles (
    url TEXT PRIMARY KEY,
    name TEXT,
    model TEXT,
    manufacturer TEXT,
    cost_in_credits TEXT,
    length TEXT,
    max_atmosphering_speed TEXT,
    crew TEXT,
    passengers TEXT,
    cargo_capacity TEXT,
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
    average_height TEXT,
    skin_colors TEXT,
    hair_colors TEXT,
    eye_colors TEXT,
    average_lifespan TEXT,
    homeworld TEXT REFERENCES planets(url),
    language TEXT,
    created TIMESTAMP,
    edited TIMESTAMP
);
