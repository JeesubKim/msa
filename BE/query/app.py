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

posts = {}

class Event(BaseModel):
    event_type: str
    data: dict


@app.get("/posts", status_code=200)
def get_query():

    return posts

@app.post("/events", status_code=201)
def write_events(body:Event):
    
    
    event_type = body.event_type
    data = body.data

    if event_type == "PostCreated":
        id = data["id"]
        
        posts[id] = {
            "id": id,
            "title": data["title"],
            "content": data["content"],
            "comments":[]
        }

    elif event_type == "CommentCreated":
        id = data["id"]
        content = data["content"]
        post_id = data["post_id"]
        status = data["status"]
        post = posts[post_id]

        post["comments"].append({
            "id":id,
            "content":content,
            "status":status
        })
    
    elif event_type == "CommentUpdated":
        id = data["id"]
        content = data["content"]
        post_id = data["post_id"]
        status = data["status"]
        post = posts[post_id]
        comments = post["comments"]
        comment = { "result": item for item in comments if item.get("id") == id }["result"]

        comment["status"] = status
        comment["content"] = content


    return { "status" : "OK" }