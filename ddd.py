from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from urllib import response
from urllib.request import Request
from fastapi import Depends, FastAPI, HTTPException, status
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import sqlite3
import os
import hashlib

DATABASE_URL = os.path.join("code/sql/proyecto.sqlite")

class Usuarios(BaseModel):
    username: str
    level: int

class home(BaseModel):
    mensaje: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class respuestas(BaseModel):
    mensaje: str

class clientesNE(BaseModel):
    nombre: str
    email: str

app = FastAPI()

security = HTTPBasic()


def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get("/", response_model=home)
async def read_root():
    return {"mensaje": "API REST"}

@app.get("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,summary="Regresa una lista de usuarios",description="Regresa una lista de usuarios")
async def read_all_items(level: int = Depends(get_current_level)):
    if level == 1: #Para usuario
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id}", response_model=Cliente,status_code=status.HTTP_202_ACCEPTED,summary="Regresa un cliente basandoso en un id dado",description="Regresa un cliente basandoso en un id dado")
async def read_an_item(id: int, level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('select * from clientes where id_cliente = {};'.format(id))
            response = cursor.fetchone()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/", response_model=respuestas,status_code=status.HTTP_202_ACCEPTED,summary="Agrega un cliente necesita nombre y email",description="Agrega un cliente necesita nombre y email")
async def add_an_item(cliente: clientesNE, level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('insert into clientes(nombre, email) values ("{}","{}");'.format(cliente.nombre,cliente.email))
            connection.commit()
            response = {
                "mensaje": "Cliente agregado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )
    
@app.put("/clientes/", response_model=respuestas,status_code=status.HTTP_202_ACCEPTED,summary="Actualizar los datos de un cliente",description="Actualizar los datos de un cliente")
async def update_an_item(cliente: Cliente,level: int = Depends(get_current_level)):
    if level == 0: #Administrador
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('update clientes set nombre = "{}", email = "{}" where id_cliente = {};'.format(cliente.nombre,cliente.email,cliente.id_cliente))
            connection.commit()
            response = {
                "mensaje": "Cliente actualizado"
            }
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.delete("/clientes/{id}",response_model=respuestas, status_code=status.HTTP_202_ACCEPTED,summary="Borrar un cliente por su id",description="Borrar un cliente por su id")
async def delete_an_item(id: int,level: int = Depends(get_current_level)):
    if level == 0:
        with sqlite3.connect('code/sql/clientes.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('delete from clientes where id_cliente = {}'.format(id))
            connection.commit()
            response = {
                "mensaje": "Cliente eliminado"
            } 
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )