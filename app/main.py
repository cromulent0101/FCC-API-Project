from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi import Body
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine
from .routers import post,user,auth
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_pwd: str = "localhost"
    database_username: str = "postgres"
    sercet_key: str = "sakd;fjasd;kjasfdjasdfasdf"

settings = Settings()

print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Hello": "test"}

