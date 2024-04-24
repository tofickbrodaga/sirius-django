# sirius-django

## Research strains - Sirius'24

### ER-schema

![photo_2024-04-23 18 38 31](https://github.com/tofickbrodaga/sirius-django/assets/101170461/cf1e1bd9-2c05-42c5-92f5-4f27b1fd8c02)




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
