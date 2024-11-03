from uuid import uuid4, UUID
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://post-clusterip-srv:4000",
    "http://comment-srv:4001",
    "http://query-srv:4002",
    "http://event-bus-srv:4005",
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

class Event(BaseModel):
    event_type: str
    data: dict

@app.get("/posts/{id}/comments", status_code=200)
def read_comments(id:str):

    return commentsByPostId.get(id, [])


@app.post("/posts/{id}/comments", status_code=201)
def write_comments(id:str, body:Comment):
    
    comment_id:UUID = str(uuid4())

    comments = commentsByPostId.get(id, [])
    
    comments.append({
        "id": comment_id,
        "content": body.content,
        "status": "pending"
    })
    commentsByPostId[id] = comments
    
    requests.post("http://event-bus-srv:4005/events", json={
        "event_type": "CommentCreated",
        "data": {
            "id": comment_id,
            "content": body.content,
            "status": "pending",
            "post_id": id,
        }
    })
    
    return commentsByPostId[id]



@app.post("/events", status_code=201)
def write_events(body:Event):
    print("Received Event", body.event_type)

    event_type = body.event_type
    data = body.data
    if event_type == "CommentModerated":
        post_id = data.get("post_id")
        id = data.get("id")
        status = data.get("status")
        content = data.get("content")
        comments:list = commentsByPostId.get(post_id, [])

        comment = { "result": item for item in comments if item.get("id") == id }["result"]

        comment["status"] = status

        print(comment)
        print(commentsByPostId)

        requests.post("http://event-bus-srv:4005/events", json={
            "event_type": "CommentUpdated",
            "data": {
                "id": id,
                "status": status,
                "content": content,
                "post_id": post_id
            }
        })
    return {}