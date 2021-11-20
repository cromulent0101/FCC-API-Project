from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi import Body
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,get_db
from .routers import post,user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "test"}

