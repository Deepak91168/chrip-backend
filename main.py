from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pymongo import MongoClient
from pydantic import BaseModel
from models.user import User
from db.connectMongo import collection
from routes.authRoute import authRoute
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from schema.messageSchema import Message
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Next.js app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRoute)

active_connections: Dict[str, WebSocket] = {}


@app.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await websocket.accept()
    active_connections[user_email] = websocket
    print(active_connections[user_email])
    print("Connection established")
    try:
        while True:
            message = await websocket.receive_json(mode='text')
            print(message['sender_email'])
            if message['recipient_email'] in active_connections:
                recipient_websocket = active_connections[message['recipient_email']]
                await recipient_websocket.send_json(data=message, mode='text')
            else:
                await websocket.send_json({"error": f"Recipient {message['recipient_email']} is not available"})
    finally:
        del active_connections[user_email]
