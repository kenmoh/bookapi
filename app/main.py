from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


from app.models import movie_model
from app.database import engine
from app.routes import movie_routes

movie_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title='MoviesAPI', description='A Simple Movie Review REST API to demonstrate microservices')

origins = [
    "http://localhost",
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def health_check():
    return {'health_status': status.HTTP_200_OK}



app.include_router(movie_routes.movie_router)
