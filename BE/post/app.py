from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4000",
    "http://localhost:4001",
    "http://localhost:3000"
]

class Post(BaseModel):
    title:str
    content:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

postsById = {}


@app.get("/posts", status_code=200)
def read_posts():
    return postsById

@app.get("/posts/{id}", status_code=200)
def read_posts_by_id(id:str):
    return postsById.get(id, [])


@app.post("/posts", status_code=201)
def write_post(post:Post):

    post_id = str(uuid4())
  
    postsById[post_id] = {
        "id":post_id,
        "title":post.title,
        "content":post.content
    }

    return postsById[post_id]


