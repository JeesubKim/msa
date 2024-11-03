from typing import Dict, Any
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



class Event(BaseModel):
    event_type: str
    data: dict


target_services = [
    "http://post-clusterip-srv:4000/events",
    "http://comment-srv:4001/events",
    "http://query-srv:4002/events",
]

@app.on_event("startup")
def startup_event():
    response = requests.get("http://event-bus-srv:4005/events")
    events = response.json()
    for event in events:
        print(event)
        event_type = event.get("event_type")
        data = event.get("data")
        handle_events(event_type, data)


@app.post("/events", status_code=201)
def write_events(body: Event):
    print("Event received: ", body.event_type)
    event_type = body.event_type
    data = body.data

    handle_events(event_type, data)    

    return { "status" : "OK" }


def handle_events(event_type, data):
    if event_type == "CommentCreated":
        status = "rejected" if "orange" in data.get("content","") else "approved"
        requests.post("http://event-bus-srv:4005/events", json={
            "event_type": "CommentModerated",
            "data": {
                "id": data.get("id"),
                "post_id": data.get("post_id"),
                "status": status,
                "content": data.get("content")
            }
        })