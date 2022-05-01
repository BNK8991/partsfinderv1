# Setup and build for DEVELOPMENT

## Clone source code

1. Clone the application:

```sh
git clone https://github.com/BNK8991/partsfinder.git
```

## Pull new source code on main branch

1. Clone the application:

```sh
git pull origin main
```

```sh
docker-compose exec partsfinder python manage.py migrate
```

```sh
docker-compose restart partsfinder worker
```

## Build

1. Build the application:

```sh
docker-compose build
```

2. Apply Django migrations:

```sh
docker-compose run --rm partsfinder python3 manage.py migrate
```

3. Init database create the admin user:

```sh
docker-compose run --rm partsfinder python3 manage.py createsuperuser
```

4. Run the application in background:

```sh
docker-compose up -d
```

5. Load data categories

```
docker-compose exec partsfinder python manage.py loaddata static/categories.json
```

5. Load data filter

```
docker-compose exec partsfinder python manage.py loaddata static/sub_categories.json
```

## make migrate

1. make a migration: after create (need folder_name) or update (not require folder_name) models

```sh
docker-compose exec partsfinder python3 manage.py makemigrations {folder_name}
```

2. run migrate: after have new migration files does not apply to db

```sh
docker-compose exec partsfinder python3 manage.py migrate
```
