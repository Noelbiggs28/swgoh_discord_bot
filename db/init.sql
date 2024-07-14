create database swgoh_database;

\connect swgoh_database

CREATE TABLE PLATOONS (
    id SERIAL PRIMARY KEY,
    phase INTEGER,
    planet VARCHAR(50),
    operations INTEGER,
    character_name VARCHAR(50)
);

CREATE TABLE PLAYERS (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50),
    ally_code VARCHAR(50)
);


CREATE TABLE PLAYERUNITS (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50),
    character_name VARCHAR(50),
    relic INTEGER,
    rarity INTEGER
);


\COPY platoons FROM '/docker-entrypoint-initdb.d/units_by_platoons.csv' WITH CSV HEADER;
\COPY players FROM '/docker-entrypoint-initdb.d/players.csv' WITH CSV HEADER;