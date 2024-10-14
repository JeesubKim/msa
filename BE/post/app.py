from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title:str
    content:str

app = FastAPI()

postsById = {}


@app.get("/posts", status_code=200)
def read_posts():
    return postsById

@app.get("/posts/{id}", status_code=200)
def read_posts_by_id():
    return postsById.get(id, [])


@app.post("/posts", status_code=201)
def write_post(post:Post):

    post_id = str(uuid4())
    posts = postsById.get(id, [])
    posts.append({
        "id":post_id,
        "title":post.title,
        "content":post.content
    })
    postsById[id] = posts

    return postsById[id]


