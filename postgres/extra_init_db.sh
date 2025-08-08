#!/bin/bash

pg_restore -U myuser -d pffdb -1 /docker-entrypoint-initdb.d/schema_backup.backup