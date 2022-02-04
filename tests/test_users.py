from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas,models
from app.config import settings
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic import command

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost:5432/fastapi-test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:   
        db.close() 

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client(session):
    # run our code before we run our test
    # command.upgrade("head",) # make sure you have the right test db env vars
    yield TestClient(app)
    # run this code after our test finishes
    #command.downgrade("base")
 
@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine) # drop all tables to prevent duplicate users
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:   
        db.close() 

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello!!!": "bind asdfasfd works"}

def test_create_user(client):
    res = client.post("/users/",json={"email": "ss@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email=="ss@gmail.com"
    assert res.status_code == 201