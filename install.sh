#!/bin/bash

# Set variables for Grafana and PostgreSQL
GRAFANA_API_KEY_NAME="my_api_key"
GRAFANA_URL="http://localhost:4569"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin"

docker network create swapi-network

docker run --name my-postgres --network swapi-network \
  -e POSTGRES_PASSWORD="postgres_password" \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres

sleep 10

cat init.sql | docker exec -i my-postgres psql -U postgres

sleep 5

python3 main.py
sleep 1
python3 rest.py

exit 0





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

sleep 15

GRAFANA_API_KEY=$(curl -X POST "$GRAFANA_URL/api/auth/keys" \
  -u "$ADMIN_USERNAME:$ADMIN_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'"$GRAFANA_API_KEY_NAME"'",
    "role": "Admin",
    "secondsToLive": 86400
  }' | jq -r '.key')

if [[ -z "$GRAFANA_API_KEY" || "$GRAFANA_API_KEY" == "null" ]]; then
  echo "Failed to create Grafana API key"
  exit 1
else
  echo "Generated Grafana API Key: $GRAFANA_API_KEY"
fi

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

CREATE_DASHBOARD_RESPONSE=$(curl -X POST "$GRAFANA_URL/api/dashboards/db" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $GRAFANA_API_KEY" \
     --data-binary "$DASHBOARD_JSON")

DASHBOARD_UID=$(echo $CREATE_DASHBOARD_RESPONSE | jq -r '.uid')

sleep 5

SNAPSHOT_RESPONSE=$(curl -X POST "$GRAFANA_URL/api/snapshots" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $GRAFANA_API_KEY" \
     --data-binary "{
         \"dashboard\": {
             \"uid\": \"$DASHBOARD_UID\",
             \"title\": \"Planet Height vs Gravity\"
         }
     }")

SNAPSHOT_URL=$(echo $SNAPSHOT_RESPONSE | jq -r '.url')
PUBLIC_SNAPSHOT_URL=$(echo $SNAPSHOT_URL | sed 's/3000/4569/')

echo "Public Snapshot URL: $PUBLIC_SNAPSHOT_URL"