from app import schemas,models
from .database import client,session

def test_root(client,session):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello!!!": "bind asdfasfd works"}

def test_create_user(client):
    res = client.post("/users/",json={"email": "ss@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email=="ss@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login",data={"username": "ss@gmail.com", "password": "password123"})
    
    ## assert new_user.email=="ss@gmail.com"
    assert res.status_code == 200