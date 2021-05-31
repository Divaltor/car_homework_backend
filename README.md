# Car homework backend

## Setup project

1. Rename .env.example to .env
2. Generate random string and set in SECRET_KEY property in .env file
    
    2.1. **Optional**: Set up password for database (not required)

3. Install [docker](https://docs.docker.com/get-docker/) and docker-compose
4. Run command: `docker-compose build && docker-compose up -d`
5. Install [poetry](https://python-poetry.org/docs/#installation)
6. Run this commands: 
   ```bash
   $ poetry install && poetry shell
   $ python manage.py migrate
   $ python manage.py seed
   $ python manage.py runserver 0.0.0.0:8001
   ```
