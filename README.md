# NFe Web App


## Setup

**Run poetry**
```bash
poetry install
poetry shell
```

**Run docker-compose**
```bash
docker-compose up -d
```

**Setup database**
```bash
RUN_AS_DB_ADMIN=true \
DB_ADMIN_USER=admin \
DB_ADMIN_PASSWORD=admin \
python manage.py create_database
```

**Migrate database**
```bash
python manage.py migrate
```

**Migrate db view**
```bash
python manage.py create_db_view
```