from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import models
from app.config import settings
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alembic import command

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345@localhost:5432/fastapi-test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


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