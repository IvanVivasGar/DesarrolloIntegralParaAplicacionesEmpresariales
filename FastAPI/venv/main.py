from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi primera chamba con APIs"

class Movie(BaseModel):
    id : int | None = None # INDICAMOS QUE ES OPCIONAL
    title : str = Field(default="Titulo Pelicula", min_length=5, max_length = 25)
    overview : str = Field(default="Esta es una sinopsis de una pelicula")
    year : str = Field(default=2000, le = 2024)
    rating : float
    category : str

    class config:
        json_schema_extra ={
            "example":{
                "id": 1,
                "title": "Titulo Pelicula",
                "overview": "Descripcion de la Pelicula",
                "year": 2023,
                "rating": 8.6,
                "category": "Action"
            }
        }

movies = [
    {
        "id": 1,
        "title":"The Godfather",
        "overview": "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        "year": "1972",
        "rating": 9.2,
        "category": "Drama"
    },
    {
        "id": 2,
        "title":"The Shawshank Redemption",
        "overview": "Two imprisoned",
        "year": "1994",
        "rating": 9.3,
        "category": "Drama"
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.get('/movies', tags=['movies'])
def get_movies() -> List[Movie]:
    return JSONResponse(content = movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge = 1, le = 2000)):
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content = item)
    return JSONResponse(content = 'Movie not found')

@app.get('/movies/', tags=['movies'], response_model = List[Movie], status_code = 200)
def get_movies_by_category(category: str = Query(min_length = 5, max_length = 15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content = data)

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content = {"message": "Se ha registrdo la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model = List[Movie], status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code = 200, content = {"message": "Se ha modificado la pelicula"})

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code = 200, content = {"message": "Se ha eliminado la pelicula"})