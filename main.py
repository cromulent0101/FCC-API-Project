# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from typing import Optional
from sys import displayhook
from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title":"title of post1", "content":"content of post 1","id":123},{"title":"fav foods","content":"pizza","id":232}]

def find_posts(id):
    for p in my_posts:
        print(p)
        if p['id'] == id:
            return p

@app.get("/")
def read_root():
    return {"Hello": "test"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,100000000)
    my_posts.append(post_dict)
    
    return {"new_post": post_dict}

@app.get("/posts/{id}")
def get_one_post(id: int,response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with {id} not found'}
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with {id} not found'}
    my_posts.remove(post)
    return({"message": f"post {id} successfully rmemoved"})
