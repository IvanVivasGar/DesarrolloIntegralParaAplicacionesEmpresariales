from fastapi import FastAPI, Body, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "PROYECTO 1er Parcial API"

# Estructura de la clase categoría
class Category(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=30)

# Estructura de la clase libro
class Book(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=30)
    author: str = Field(min_length=1, max_length=50)
    year: str
    category: Category
    pages: int = Field(ge=1)

# Lista de libros y categorías inicializada con algunos valores
books = [
    {
        "id": 1,
        "title": "Harry Potter y la Cámara de los secretos",
        "author": "J.K Rowling",
        "year": 1998,
        "category": {
            "id": 1,
            "name": "Fantasía",
        },
        "pages": 320,
    },
    {
        "id": 2,
        "title": "Harry Potter y la piedra filosofal",
        "author": "J.K Rowling",
        "year": 1997,
        "category": {
            "id": 1,
            "name": "Fantasía",
        },
        "pages": 320,
    }
]

categories = [
    {
        "id": 1,
        "name": "Fantasía",
    },
    {
        "id": 2,
        "name": "Misterio",
    }
]

# Retorna todos los libros registrados
@app.get("/books", tags=["Books"], response_model=List[Book], status_code=200)
def get_books() -> List[Book]:
    return JSONResponse(content=books, status_code=200)

# Buscar libros por id
@app.get("/books/{id}", tags=["Books"], status_code=200)
def get_book_id(id: int = Path(..., ge=1, le=2000)):
    for item in books:
        if item['id'] == id:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=400, content={"message": "No existe un libro con ese identificador."})

# Buscar libros por categoría
@app.get("/books_by_category/", tags=["Books"], response_model=List[Book], status_code=200)
def get_books_by_category(category: str = Query(..., min_length=1)):
    data = [item for item in books if item['category']['name'].lower().strip() == category.lower().strip()]
    return JSONResponse(content=data)

# Crea un nuevo libro
@app.post("/books/", tags=["Books"], status_code=200)
def create_book(title: str = Body(...), author: str = Body(...), year: str = Body(...), category: int = Body(...), pages: int = Body(...)):
    # Verificar si la categoría existe
    categoria_encontrada = next((cat for cat in categories if cat["id"] == category), None)
    if not categoria_encontrada:
        raise HTTPException(status_code=400, detail="Categoría no válida. Debe crear esta categoría antes de agregar el libro.")
    
    # Verificar si el ID del libro ya existe
    if any(book["id"] == category for book in books):
        raise HTTPException(status_code=400, detail="Ya existe un libro con este ID.")

    # Crear un nuevo libro
    new_book = {
        "id": category,
        "title": title,
        "author": author,
        "year": year,
        "category": {"id": category, "name": categoria_encontrada["name"]},
        "pages": pages,
    }
    books.append(new_book)
    return JSONResponse(status_code=200, content={"message": "Libro creado exitosamente."})

# Modifica un libro
@app.put('/books/{id}', tags=["Books"], status_code=200)
def modify_book(id: int = Path(..., ge=1), title: str = Body(...), author: str = Body(...), year: str = Body(...), category: str = Body(...), pages: int = Body(...)):
    # Verificar si la categoría existe
    if not any(cat["name"].lower().strip() == category.lower().strip() for cat in categories):
        raise HTTPException(status_code=400, detail=f"La categoría '{category}' no existe.")
    
    # Verificar si el libro existe
    if not any(book['id'] == id for book in books):
        raise HTTPException(status_code=400, detail=f"El libro con el id {id} no existe.")
    
    # Modificar el libro con el id proporcionado
    for book in books:
        if book['id'] == id:
            book['title'] = title
            book['author'] = author
            book['year'] = year
            book['category'] = category
            book['pages'] = pages
            return JSONResponse(status_code=200, content={"message": f"El libro con el id {id} se ha actualizado."})

# Eliminar un libro
@app.delete('/books/{id}', tags=["Books"], status_code=200)
def delete_book(id: int = Path(..., title="ID del libro", description="ID del libro a eliminar")):
    global books
    books = [book for book in books if book['id'] != id]
    return JSONResponse(status_code=200, content={"message": f"El libro con el id {id} se ha eliminado."})

# Retorna todas las categorías
@app.get("/categories", tags=["Categories"], response_model=List[Category], status_code=200)
def get_categories() -> List[Category]:
    return JSONResponse(content=categories, status_code=200)

# Crea una nueva categoría
@app.post('/categories', tags=["Categories"], status_code=200)
def create_category(name: str = Query(..., min_length=1)):
    # Verificar si la categoría ya existe
    if any(cat["name"].lower().strip() == name.lower().strip() for cat in categories):
        raise HTTPException(status_code=400, detail="Esa categoría ya existe.")
    
    # Crear una nueva categoría
    new_category_id = max(cat["id"] for cat in categories) + 1
    new_category = {"id": new_category_id, "name": name}
    categories.append(new_category)
    return JSONResponse(status_code=200, content={"message": "Categoría agregada con éxito."})

# Eliminar una categoría
@app.delete('/categories/{id}', tags=["Categories"], status_code=200)
def delete_category(id: int = Path(..., title="ID de la categoría", description="ID de la categoría a eliminar")):
    global categories
    global books
    
    # Verificar si la categoría tiene libros asociados
    if any(book['category']['id'] == id for book in books):
        raise HTTPException(status_code=400, detail="La categoría tiene libros asociados. No se puede eliminar.")
    
    # Eliminar la categoría
    categories = [cat for cat in categories if cat['id'] != id]
    return JSONResponse(status_code=200, content={"message": f"La categoría con el ID {id} se ha eliminado correctamente."})

# Modificar una categoría
@app.put('/categories/{id}', tags=["Categories"], status_code=200)
def modify_category(id: int = Path(..., title="ID de la categoría", description="ID de la categoría a modificar"), name: str = Query(..., min_length=1)):
    global categories
    global books
    
    # Verificar si la categoría existe
    category = next((cat for cat in categories if cat["id"] == id), None)
    if category is None:
        raise HTTPException(status_code=404, detail=f"La categoría con el ID {id} no existe.")
    
    # Verificar si el nombre de la categoría ya existe
    if any(cat["name"].lower().strip() == name.lower().strip() for cat in categories if cat["id"] != id):
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre.")
    
    # Modificar el nombre de la categoría
    category["name"] = name
    
    # Modificar el nombre de la categoría en todos los libros asociados
    for book in books:
        if book["category"]["id"] == id:
            book["category"]["name"] = name
    
    return JSONResponse(status_code=200, content={"message": f"La categoría con el ID {id} se ha modificado correctamente."})