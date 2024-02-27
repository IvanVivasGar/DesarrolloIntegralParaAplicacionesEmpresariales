# TODO Realizar los endpoints para la venta de computadoras con una lista de 5 registros con los siguientes campos
# TODO - id
# TODO - marca
# TODO - modelo
# TODO - color
# TODO - ram
# TODO - almacenamiento
# TODO Realiza los endpoints ya hechos en clase, en lugar de get by categoria sera get by marca, de manera que se obtenga
# TODO todo el cuerpo de la computadora por la marca, en caso de ser mas de una, mostrara todas las que sean de la misma marca

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Venta de Computadoras"

# Lista de computadoras
computadoras = [
    {
        id: 0,
        "marca":"Asus",
        "modelo": "Republic of Gamers",
        "color": "Blanca",
        "ram": 16,
        "almacenamiento": "1TB"
    },
    {
        id: 1,
        "marca":"HP",
        "modelo": "Pavilion",
        "color": "Negra",
        "ram": 8,
        "almacenamiento": "500GB"
    },
    {
        id: 2,
        "marca":"HP",
        "modelo": "Vector",
        "color": "Gris",
        "ram": 4,
        "almacenamiento": "250GB"
    },
    {
        id: 3,
        "marca":"Acer",
        "modelo": "Aspire",
        "color": "Azul",
        "ram": 12,
        "almacenamiento": "750GB"
    },
    {
        id: 4,
        "marca":"Lenovo",
        "modelo": "IdeaPad",
        "color": "Roja",
        "ram": 6,
        "almacenamiento": "350GB"
    }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

# Endpoints
# Obtener todas las computadoras
@app.get('/computadoras', tags=["computadoras"])
def get_computadoras():
    return computadoras

# Obtener una computadora por id
@app.get('/computadoras/{id}', tags=["computadoras"])
def get_computadora(id: int):
    for item in computadoras:
        if item['id'] == id:
            return item
    return {'message': 'Computadora no encontrada'}

# Obtener computadoras por marca
@app.get('/computadoras/', tags=['computadoras'])
def get_computadora_by_marca(marca: str):
    lista_computadoras = []
    for item in computadoras:
        if item['marca'] == marca:
            lista_computadoras.append(item)
    return lista_computadoras