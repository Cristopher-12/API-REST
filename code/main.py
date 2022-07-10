from fastapi import Depends, FastAPI, HTTPException, status
import sqlite3
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import os
import hashlib
from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from urllib import response
from urllib.request import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() 

DATABASE_URL = os.path.join("sql/clientes.sqlite") 

security = HTTPBasic() 


class Respuesta (BaseModel) :  
    message: str  
           
class Cliente (BaseModel):  
    id_cliente: int  
    nombre: str  
    email: str  

class Agregar_cliente(BaseModel):
    nombre: str
    email : str

origin = [
    "https://8000-cristopher12-apirest-datmbv7hpqx.ws-us53.gitpod.io/",
    "https://8080-cristopher12-apirest-datmbv7hpqx.ws-us53.gitpod.io/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),)
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0] #ADMIN

@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 

@app.get("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
summary="Regresa la lista",description="Regresa la lista")
async def get_clientes(level: int = Depends(get_current_level)):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id}", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
summary="Regresa la lista",description="Regresa la lista")
async def get_cliente_id(id_cliente: int=0, level: int = Depends(get_current_level)):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(id_cliente))
            response = cursor.fetchall()
            if response is None:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail      = "Cliente not found",
                    headers     = {"WWW-Authenticate": "Basic"},
                )
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.post("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
summary="Inserta usuario",description="Inserta usuario")
async def post_clientes(cliente: Agregar_cliente, level: int = Depends(get_current_level)):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email) VALUES (? , ?);",(cliente.nombre, cliente.email))
            connection.commit()
            response = {"message":"Cliente agregado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )
@app.put("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
summary="Actualiza usuario",description="Actualiza usuario")
async def put_clientes(cliente: Cliente, level: int = Depends(get_current_level)):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(cliente.nombre, cliente.email, cliente.id_cliente))
            connection.commit()
            response = {"message":"Cliente actualizado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.delete("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
summary="Elimina usuario",description="Elimina usuario")
async def delete_clientes(level: int = Depends(get_current_level), id_cliente: int=0):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente= '{id_cliente}';".format(id_cliente=id_cliente))
            connection.commit()
            response = {"message":"Cliente eliminado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )