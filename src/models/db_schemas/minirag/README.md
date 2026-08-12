## Run Alembic migrations

###configrations


cp alembic.ini.example alembic.ini

-Update alembic.ini file with your database credentials(sqlalchemy.url)


### optional new migrations


### make revision
- make revision

```bash

alembic revision --autogenerate -m "initial commit"
```
### upgrade data base
- upgrade database

```bash
alembic upgrade head
```




