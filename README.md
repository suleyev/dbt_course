# dbt_course

## First run

1. Install git and docker compose
2. Create virtual environment for python packages and install deps from requirements.txt
3. Copy dbt/profiles.yml file into ~/.dbt/profiles.yml
   ```shell
   cp dbt/profiles.yml ~/.dbt/profiles.yml
   ```
4. Start docker containers with docker compose
   ```shell
   docker compose up -d --build
   docker compose logs -f prepare_dwh_app
   ```
5. Execute DBT commands
   ```shell
   dbt deps --project-dir dbt
   dbt run --project-dir dbt
   dbt test --project-dir dbt
   dbt docs generate --project-dir dbt && dbt docs serve --port 12302 --project-dir dbt
   ```


