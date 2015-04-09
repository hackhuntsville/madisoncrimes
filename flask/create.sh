#!/usr/bin/env bash

#CID=$(docker run -e USERNAME=docker -e PASS=docker -d -v ~/postgres_data:/var/lib/postgresql -t postgis:2.1);
CID='berserk_bardeen'
DB_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' ${CID})

createdb -h ${DB_IP} -U docker madison_gis
psql -d madison_gis -h ${DB_IP} -U docker -c "CREATE EXTENSION postgis;"

