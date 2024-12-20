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
    "http://moderation-srv:4003/events",
]

events = []

@app.post("/events", status_code=201)
def write_events(body: Event):
    print("Event received: ", body.event_type)
    
    events.append(body)

    for service in target_services:
        
        requests.post(service, json=body.dict())


    return { "status" : "OK" }



@app.get("/events", status_code=200)
def read_events():
    return events