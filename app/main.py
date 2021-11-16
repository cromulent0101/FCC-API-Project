# pylint: skip-file
from typing import Optional
from sys import displayhook
from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='passwod123', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('connected to db successful')
        break;
    except Exception as error:
        print('Connection to db failed')
        print('error = ',error)
        time.sleep(3)
        
my_posts = [{"title":"title of post1", "content":"content of post 1","id":123},{"title":"fav foods","content":"pizza","id":232}]

def find_post(id):
    for p in my_posts:
        print(p)
        if p['id'] == id:
            return p


def find_index(id): 
    for p in my_posts:
        print(p)
        if p['id'] == id:
            return my_posts.index(p)

@app.get("/")
def read_root():
    return {"Hello": "test"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"new_post": new_post}

@app.get("/posts/{id}")
def get_one_post(id: int,response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with {id} not found'}
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s returning *""" % (str(id)),)
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')

    conn.commit()
    return({"message": f"post {id} successfully rmemoved"})

@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
def update_post(id: int,post: Post):
    cursor.execute("""UPDATE posts SET title = \'%s\', content = \'%s\', published = %s WHERE id = %s RETURNING *""" % (post.title, post.content, post.published, str(id)),)
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    conn.commit()
    return {"message": updated_post}
