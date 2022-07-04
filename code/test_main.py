from urllib import response
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API-REST"}

def test_get_all():
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert response.json() == [{"id_cliente":1,"nombre":"Cristopher","email":"cristopher@email.com"},{"id_cliente":2,"nombre":"Sebastian","email":"sebastian@email.com"},{"id_cliente":3,"nombre":"Arturo","email":"arturo@email.com"}]
                            
def test_get_id():
    response = client.get("/clientes/2")
    assert response.status_code == 200
    assert response.json() == {"id_cliente":2,"nombre":"Sebastian","email":"sebastian@email.com"}

def test_post():
    data = {"nombre":"test","email":"test@test.com"}
    response = client.post("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message":"Cliente Agregado"}

def test_put():
    data = {"id_cliente": 12,"nombre":"changed","email":"changed@changed.com"}
    response = client.put("/clientes/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message":"Cliente Actualizado"}

def test_delete():
    response = client.delete("/clientes/12")
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente eliminado"} 

