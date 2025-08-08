FROM postgres:17

RUN apt-get update &&  \
    apt-get -y install postgresql-17-cron

RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample \
    && echo "cron.database_name = 'pffdb'" >> /usr/share/postgresql/postgresql.conf.sample

COPY extra_init_db.sh /docker-entrypoint-initdb.d/
COPY schema_backup.backup /docker-entrypoint-initdb.d/