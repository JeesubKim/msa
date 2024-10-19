from typing import Dict, Any
from uuid import uuid4, UUID
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4000", #post
    "http://localhost:4001", #comment
    "http://localhost:4002", #query
    "http://localhost:4003", #moderation

    "http://localhost:4005", #event-bus
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



class Event(BaseModel):
    event_type: str
    data: dict


target_services = [
    "http://localhost:4000/events",
    "http://localhost:4001/events",
    "http://localhost:4002/events",
]

@app.post("/events", status_code=201)
def write_events(body: Event):
    print("Event received: ", body.event_type)
    event_type = body.event_type
    data = body.data
    if event_type == "CommentCreated":
        status = "rejected" if "orange" in data.get("content","") else "approved"
        requests.post("http://localhost:4005/events", json={
            "event_type": "CommentModerated",
            "data": {
                "id": data.get("id"),
                "post_id": data.get("post_id"),
                "status": status,
                "content": data.get("content")
            }
        })


    return { "status" : "OK" }