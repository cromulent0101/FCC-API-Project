from typing import Optional
from sys import displayhook
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "test"}

@app.get("/posts")
def get_posts():
    return {"item_id": "this is your posts"}

print("committing from CLI worked, so trying from VSC")