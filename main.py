# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from typing import Optional
from sys import displayhook
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "test"}

@app.get("/posts")
def get_posts():
    return {"item_id": "this is your posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"new_post": post}
