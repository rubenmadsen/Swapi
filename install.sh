#!/bin/bash

# Prompt for the PostgreSQL password
read -sp "Choose your () PostgreSQL password: " POSTGRES_PASSWORD
echo
export POSTGRES_PASSWORD
#docker run --name my-postgres -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -v pgdata:/var/lib/postgresql/data -p 5432:5432 -d postgres


#docker pull postgres
#pip install psycopg2-binary
#pip install requests