from uuid import uuid4, UUID
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
commentsByPostId = {}

class Comment(BaseModel):
    content:str


@app.get("/posts/{id}/comments", status_code=200)
def read_comments(id:str):

    return commentsByPostId.get(id, [])


@app.post("/posts/{id}/comments", status_code=201)
def write_comments(id:str, body:Comment):
    print(body)
    comment_id:UUID = str(uuid4())

    comments = commentsByPostId.get(id, [])
    
    comments.append({
        "id": comment_id,
        "comment": body.content
    })
    commentsByPostId[id] = comments

    return commentsByPostId[id]