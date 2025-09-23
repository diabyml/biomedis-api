## TEST SETUP

- python test_setup.py

## Generate the initial migration

alembic revision --autogenerate -m "Initial migration"

## Apply the migration to create tables

alembic upgrade head

## Run app

# Start the development server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
