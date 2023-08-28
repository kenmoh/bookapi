echo"Preparing migrations ..."
alembic revisions --autogenerate -m'Initial migrations'

echo"Running migrations..."
alembic upgrade head

echo"Start the server ..."
uvicorn app.main:app --host 0.0.0.0 --reload