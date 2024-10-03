#!/bin/bash

# Set variables for Grafana and PostgreSQL
GRAFANA_API_KEY_NAME="my_api_key"
GRAFANA_URL="http://localhost:4569"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin"

# Create a Docker network
docker network create swapi-network

# Run PostgreSQL in Docker
docker run --name my-postgres --network swapi-network \
  -e POSTGRES_PASSWORD="postgres_password" \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres

# Wait for the PostgreSQL container to start
sleep 10

# Initialize the PostgreSQL database
cat init.sql | docker exec -i my-postgres psql -U postgres

# Wait for the initialization to complete
sleep 5

# Run your Python script to fetch data
python3 main.py

# Run Grafana in Docker with port binding to 4569 externally
docker run --name my-grafana --network swapi-network \
  -p 4569:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=$ADMIN_PASSWORD" \
  -e "GF_SECURITY_ADMIN_USER=$ADMIN_USERNAME" \
  -e "GF_AUTH_ANONYMOUS_ENABLED=true" \
  -e "GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer" \
  -e "GF_SNAPSHOTS_PUBLIC_MODE=true" \
  -e "GF_SNAPSHOTS_EXTERNAL_ENABLED=true" \
  -v grafana-storage:/var/lib/grafana \
  -d grafana/grafana

# Wait for Grafana to start
sleep 15

# Create Grafana API key
GRAFANA_API_KEY=$(curl -X POST "$GRAFANA_URL/api/auth/keys" \
  -u "$ADMIN_USERNAME:$ADMIN_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$GRAFANA_API_KEY_NAME"'",
    "role": "Admin",
    "secondsToLive": 86400
  }' | jq -r '.key')

# Check if the API key was created successfully
if [[ -z "$GRAFANA_API_KEY" || "$GRAFANA_API_KEY" == "null" ]]; then
  echo "Failed to create Grafana API key"
  exit 1
else
  echo "Generated Grafana API Key: $GRAFANA_API_KEY"
fi

# Set up the PostgreSQL datasource in Grafana
curl -X POST "$GRAFANA_URL/api/datasources" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -d '{
        "name": "PostgreSQL",
        "type": "postgres",
        "url": "my-postgres:5432",
        "access": "proxy",
        "basicAuth": false,
        "database": "postgres",
        "user": "postgres",
        "password": "postgres_password",
        "jsonData": {
          "sslmode": "disable"
        }
      }'

# Dashboard creation JSON
DASHBOARD_JSON=$(cat <<EOF
{
  "dashboard": {
    "id": null,
    "uid": null,
    "title": "Planet Height vs Gravity",
    "tags": [],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 0,
    "panels": [
      {
        "datasource": "PostgreSQL",
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "palette-classic"
            },
            "custom": {}
          },
          "overrides": []
        },
        "gridPos": {
          "h": 9,
          "w": 12,
          "x": 0,
          "y": 0
        },
        "id": 2,
        "options": {
          "showLines": true,
          "showPoints": true,
          "fillOpacity": 0
        },
        "targets": [
          {
            "refId": "A",
            "rawSql": "SELECT planets.gravity AS x, AVG(characters.height) AS y FROM characters JOIN planets ON characters.homeworld = planets.url GROUP BY planets.gravity",
            "format": "table"
          }
        ],
        "title": "Height vs Gravity",
        "type": "timeseries"
      }
    ]
  },
  "overwrite": false
}
EOF
)

# Use curl to create the dashboard
CREATE_DASHBOARD_RESPONSE=$(curl -X POST "$GRAFANA_URL/api/dashboards/db" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $GRAFANA_API_KEY" \
     --data-binary "$DASHBOARD_JSON")

# Extract the UID from the response
DASHBOARD_UID=$(echo $CREATE_DASHBOARD_RESPONSE | jq -r '.uid')

# Wait for the dashboard to be created
sleep 5

# Create a snapshot for public sharing
SNAPSHOT_RESPONSE=$(curl -X POST "$GRAFANA_URL/api/snapshots" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $GRAFANA_API_KEY" \
     --data-binary "{
         \"dashboard\": {
             \"uid\": \"$DASHBOARD_UID\",
             \"title\": \"Planet Height vs Gravity\"
         }
     }")

# Extract the snapshot URL from the response
SNAPSHOT_URL=$(echo $SNAPSHOT_RESPONSE | jq -r '.url')
PUBLIC_SNAPSHOT_URL=$(echo $SNAPSHOT_URL | sed 's/3000/4569/')

# Output the snapshot URL (public link)
echo "Public Snapshot URL: $PUBLIC_SNAPSHOT_URL"