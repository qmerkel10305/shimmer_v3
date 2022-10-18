FROM postgis/postgis:12-3.0

COPY tables.sql /docker-entrypoint-initdb.d/
COPY docker_config/setup.sql /docker-entrypoint-initdb.d/

COPY docker_config/pg_hba.conf /etc/postgresql/12/main/
COPY docker_config/pg_ident.conf /etc/postgresql/12/main/
COPY docker_config/postgresql.conf /etc/postgresql/12/main/
