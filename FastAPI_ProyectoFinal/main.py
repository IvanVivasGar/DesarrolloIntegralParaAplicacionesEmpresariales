from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "PROYECTO 1er Parcial API"


books = []
    # {
    #     "id" : 1,
    #     "title" : "harry potter and the chamber of secrets",
    #     "author" : "k.K Rowling",
    #     "year" : 1998,
    #     "category" : {
    #         "id": 1,
    #         "name": "Fantasia",
    #     },
    #     "pages" : 251,
    # },
    # {
    #     "id" : 2,
    #     "title" : "harry potter philosopher's stone",
    #     "author" : "J.K Rowling",
    #     "year" : 1997,
    #     "category" : {
    #         "id": 1,
    #         "name": "Fantasia",
    #     },
    #     "pages" : 320,
    # }

categories = []
    # {
    #     "id": 1,
    #     "name": "Fantasia",
    # },
    # {
    #     "id": 2,
    #     "name": "Misterio",
    # }


class Category(BaseModel):
    id : int = Field(ge = 1)
    name : str = Field(min_length = 1, max_length = 30)
    class config:
        json_schema_extra = {
            "category" : {
                "id" : 1,
                "name" : "Misterio"
            }
        }

# Estructura de la clase libro
class Book(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1,max_length=30)
    author: str = Field(min_length=1,max_length=50)
    year: str
    category: Category
    pages: int = Field(ge=1)
    class config:

        json_schema_extra = {
            "book":{
                "title": "Titulo del libro",
                "author": "Autor del libro",
                "year": "Año de publicacion",
                "category": {
                    "id" : 1,
                    "name" : "Misterio"
                },
                "pages": 1
            }
        }

# Contador global para id
        
class AutoIncrement:
    _id = 0

    @classmethod
    def get_id(cls):
        cls._id += 1
        return cls._id
    
    def delete_int(cls):
        cls._id -= 1
        return cls._id

auto_increment_id_categories = AutoIncrement()
auto_increment_id_books = AutoIncrement()  
# auto_increment_id_categories = len(categories) + 1
# next_book_id = len(books) + 1

# =========Seccion Books=========

# Retorna todos los libros registrados
@app.get("/books", tags = ["Books"], response_model = List[Book], status_code = 200)
def get_books() -> List[Book]:
    return JSONResponse(content = books, status_code=200)

# Buscar libros por id
@app.get("/books/{id}", tags = ["Books"])
def get_book_id(id : int = Path(ge = 1, le = 2000)):
    for item in books:
        if item['id'] == id:
            return JSONResponse(status_code = 200, content = item)
    return JSONResponse(status_code = 400, content = {"message" : "No existe un libro con ese identificador."})

# Buscar libros por categoria
@app.get("/books/", tags = ["Books"], response_model = List[Book], status_code = 200)
def get_book_category(category : str = Query) -> List[Book]:
    data = [item for item in books if item['category']['name'].lower().strip().replace(" ", "") == category.lower().strip().replace(" ", "")]
    return JSONResponse(content = data)

# ==============Seccion categorias==============

# Retorna todas las categorias
@app.get("/categories", tags = ["Categories"], response_model = List[Category], status_code = 200)
def get_categories() -> List[Category]:
    return JSONResponse(content=categories,status_code = 200)

# Crea categorias solo si no existen
@app.post('/categories', tags = ["Categories"])
def create_category(name: str = Query):
    # Variable id se auto incremento
    global auto_increment_id_categories 
    for item in categories:
        if name.lower().strip().replace(" ", "") == item["name"].lower().strip().replace(" ", ""):
            return JSONResponse(statuscode = 400, content = {"message" : "Esa categoria ya existe."})
    new_category = {"id": auto_increment_id_categories.get_id(), "name" : name}
    categories.append(new_category)

    return JSONResponse(status_code = 200, content = {"message" : "Categoria agregada con exito"})

# Eliminar la categoria, solo si no tiene ningun libro dentro
@app.delete('/categories/{name}', tags = ["Categories"])
def delete_category(name : str = Query):
    global auto_increment_id_categories
    for item in categories:
        if item['name'].lower().strip().replace(" ", "") == name.lower().strip().replace(" ", ""):
            for item in books:
                if item['category']['name'].lower().strip().replace(" ", "") == name.lower().strip().replace(" ", ""):
                    return JSONResponse(status_code = 400, content = {"message" : "La categoria tiene libros afiliados, no se puede eliminar."})
            auto_increment_id_categories.delete_int
            categories.remove(item)

            for index, category in enumerate(categories, start=1):
                category['id'] = index
            return JSONResponse(status_code = 200, content = {"message" : "La categoria se elimino correctamente"})
    return JSONResponse(status_code = 400, content = {"message" : "No existe tal categoria"})

# Modificar categorias
@app.put('/categories/{name}', tags = ["Categories"], status_code = 200)
def modify_category(name : str = Query, newName : str = Query):
    for item in categories:
        if item["name"].lower().strip().replace(" ", "") == name.lower().strip().replace(" ", ""):
            item["name"] = newName
            return JSONResponse(status_code = 200, content = item)
        
