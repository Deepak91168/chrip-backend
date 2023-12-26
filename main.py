from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pymongo import MongoClient
from pydantic import BaseModel
from models.user import User
from db.connectMongo import user_collection, conversation_collection
from routes.authRoute import authRoute
from routes.userRoute import userRoute
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
app.include_router(userRoute)

active_connections: Dict[str, WebSocket] = {}


def save_message_to_db(message: Message):
    message_dict = message.dict()
    result = conversation_collection.insert_one(message_dict)
    print(f"result:{result.inserted_id}")


def get_chat_history(sender_email: str, recipient_email: str):
    chat_history = conversation_collection.find(
        {"$or": [{"sender_email": sender_email, "recipient_email": recipient_email},
                 {"sender_email": recipient_email, "recipient_email": sender_email}]})
    return chat_history

@app.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str):
    await websocket.accept()
    active_connections[user_email] = websocket
    if user_email in active_connections:
        print(active_connections[user_email])
        print("user is online")
    try:
        while True:
            message = await websocket.receive_json(mode='text')
            new_message = Message(**message)
            save_message_to_db(new_message)
            if message['recipient_email'] in active_connections:
                recipient_websocket = active_connections[message['recipient_email']]
                await recipient_websocket.send_json(data=message, mode='text')
            else:
                await websocket.send_json({"error": f"Recipient {message['recipient_email']} is not available"})
    finally:
        del active_connections[user_email]

