from uuid import uuid4, UUID
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4000",
    "http://localhost:4001",
    "http://localhost:4002",
    "http://localhost:4005",
    "http://localhost:3000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

commentsByPostId = {}

class Comment(BaseModel):
    content:str

class CommentEventData(BaseModel):
    id:str
    content:str
    post_id:str

class Event(BaseModel):
    event_type: str
    data: CommentEventData

@app.get("/posts/{id}/comments", status_code=200)
def read_comments(id:str):

    return commentsByPostId.get(id, [])


@app.post("/posts/{id}/comments", status_code=201)
def write_comments(id:str, body:Comment):
    
    comment_id:UUID = str(uuid4())

    comments = commentsByPostId.get(id, [])
    
    comments.append({
        "id": comment_id,
        "content": body.content
    })
    commentsByPostId[id] = comments
    
    requests.post("http://localhost:4005/events", json={
        "event_type":"CommentCreated",
        "data": {
            "id": comment_id,
            "content": body.content,
            "post_id": id
        }
    })
    
    return commentsByPostId[id]



@app.post("/events", status_code=201)
def write_events(body:Event):
    print("Received Event", body.type)

    return {}