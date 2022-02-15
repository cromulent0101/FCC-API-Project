from app import schemas,models,oauth2
from .database import client,session
from jose import jwt
from fastapi import HTTPException
import pytest

# def test_root(client,session):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Hello!!!": "bind asdfasfd works"}



def test_create_user(client):
    res = client.post("/users/",json={"email": "ss@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email=="ss@gmail.com"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login",data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    try:
        token_data = oauth2.verify_access_token(login_res.access_token,HTTPException)
        print('it worked')
    except HTTPException:
        print('bad token')

    # payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    # id = payload.get('user_id')
    ## assert new_user.email=="ss@gmail.com"
    assert token_data.id == test_user['id']
    assert login_res.token_type=='bearer'
    assert res.status_code == 200