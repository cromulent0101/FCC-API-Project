from app import schemas,models,oauth2
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

@pytest.mark.parametrize('email,password,status_code',[
    ('wrongemail@email.com','password123',403),
    ('bob123@email.com','bob123',403),
    ('ss@gmail.com','asdf',403),
    (None,'password123',422),
    ('ss@gmail.com',None,422)
])
def test_incorrect_login(client, test_user,email,password,status_code):
    res = client.post("/login", data={'username': email, 'password': password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'