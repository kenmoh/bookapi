from fastapi import FastAPI, status

from app.models import book_model
from app.database import engine

book_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title='BooksAPI', description='A Simple books REST API to demonstrate microservices')


@app.get('/')
async def health_check():
    return {'health_status': status.HTTP_200_OK}
