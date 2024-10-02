#!/bin/bash

# Prompt for the PostgreSQL password
#read -sp "Choose your () PostgreSQL password: " POSTGRES_PASSWORD
#echo
#export POSTGRES_PASSWORD
docker run --name my-postgres -e POSTGRES_PASSWORD="postgres_password" -v pgdata:/var/lib/postgresql/data -p 5432:5432 -d postgres
sleep 3
#cat init.sql | docker exec -i my-postgres psql -U postgres
sleep 2
python3 main.py

