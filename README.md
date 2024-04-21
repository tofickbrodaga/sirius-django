# sirius-django

## Research strains - Sirius'24

### ER-schema

![database_bio](https://github.com/tofickbrodaga/sirius-django/assets/101170461/7bb2a722-ffe5-42d5-b0ec-d58b8f727fa1)

### Create docker
```
docker run -d --name project -p 5435:5432 \
-e POSTGRES_USER=app \
-e POSTGRES_PASSWORD=123 \
-e POSTGRES_DB=project_db \
postgres
```
### Connection
```
psql -h 127.0.0.1 -p 5435 -U app project_db
```
### Initial database
```
psql -h 127.0.0.1 -p 5435 -U app project_db -f init_db.ddl ??????
```