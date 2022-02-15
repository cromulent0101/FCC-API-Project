from app import schemas,models,oauth2
from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost:5432/fastapi-test' # could pull this from settings

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email": "ss@gmail.com", "password": "password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password']=user_data['password'] # add pwd to response
    return new_user

@pytest.fixture(scope="function")
def client(session):
    # run our code before we run our test
    # command.upgrade("head",) # make sure you have the right test db env vars
    print("my session fixture ran")

    def override_get_db():
        try:
            yield session
        finally:   
            session.close() 
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run this code after our test finishes
    #command.downgrade("base")
 
@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    models.Base.metadata.drop_all(bind=engine) # drop all tables to prevent duplicate users
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:   
        db.close() 

