from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine
from .routers import post,user,auth,vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

origins = ["*"] # no header unless this is star?/?

ware = [Middleware(CORSMiddleware, 
        allow_origins=origins, 
        allow_credentials=True, 
        allow_methods=['*'], 
        allow_headers=['*'])]

app = FastAPI(middleware=ware)
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"Hello": "test"}

