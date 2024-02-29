from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi primera chamba con APIs"

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
def message():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    return {'message': 'Movie not found'}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return category

@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies
