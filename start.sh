#!/bin/bash

docker-compose up -d  --build
docker-compose logs -f prepare_dwh_app

dbt run --project-dir dbt
dbt test --project-dir dbt
dbt docs generate --project-dir dbt && dbt docs serve --port 12302 --project-dir dbt