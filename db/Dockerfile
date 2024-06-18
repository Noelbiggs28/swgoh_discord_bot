FROM postgres:15

WORKDIR /docker-entrypoint-initdb.d

COPY units_by_platoons.csv .
COPY players.csv .
COPY init.sql .
