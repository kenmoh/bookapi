from fastapi import FastAPI, status

from app.models import movie_model
from app.database import engine
from app.routes import movie_routes

movie_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title='MoviesAPI', description='A Simple Movie Review REST API to demonstrate microservices')


@app.get('/')
async def health_check():
    return {'health_status': status.HTTP_200_OK}

app.include_router(movie_routes.movie_router)
