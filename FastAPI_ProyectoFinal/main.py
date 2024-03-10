from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "PROYECTO 1er Parcial API"


books = [
    {
        "id" : 1,
        "title" : "harry potter and the chamber of secrets",
        "author" : "k.K Rowling",
        "year" : 1998,
        "category" : "fantasy",
        "pages" : 251,
    },
    {
        "id" : 2,
        "title" : "harry potter philosopher's stone",
        "author" : "J.K Rowling",
        "year" : 1997,
        "category" : "fantasy",
        "pages" : 320,
    }
]

categories = [
    {
        "id":1,
        "name": "fantasy",
    }
]

class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1,max_length=30)
    author: str = Field(min_length=1,max_length=50)
    year: int
    category: str = Field(min_length=1,max_length=50)
    pages: int = Field(ge=1)
    class Config:

        json_shcema_extra = {
            "book":{
                "title":"",
                "author":"",
                "year":"",
                "category":"",
                "pages":""
            }
        }


class Category(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=1, max_lengt = 25)
    class Config:

        json_shcema_extra = {
            "category":{
            "name":""
            }
        }


@app.get("/books", tags=["books"], response_model = List[Book],status_code = 200)
def get_books() -> List[Book]:
    return JSONResponse(content=books,status_code=200)

@app.get("/categories", tags=["categories"], response_model = List[Category], status_code = 200)
def get_categories() -> List[Category]:
    return JSONResponse(content=categories,status_code = 200)

@app.post('/categories', tags = ["categories"])
def create_category(category: Category) -> dict:
    for item in categories:
        if category == categories[item]:
            return JSONResponse(statuscode = 400, content = {"message" : "Esa categoria ya existe."})
    categories.append(category)

@app.delete('/categories', tags = ["categories"])
def delete_category(category: Category) -> dict:
    for item in categories:
        if category == categories[item]:
            categories.remove(item)