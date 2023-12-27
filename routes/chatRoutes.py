from models.user import User
from db.connectMongo import user_collection
from fastapi import APIRouter,Depends, HTTPException, Response, Request
from utils.security.security import hash_password, verify_password
from utils.auth.token import create_access_token, decode_token
from middlewares.auth.isAuthenticated import isAuthenticated
from datetime import datetime, timedelta
from schema.google_auth import GoogleLoginRequestUser
from db.connectMongo import conversation_collection

chatRoute = APIRouter()

@chatRoute.get("/chat/get-chat-history")
async def get_chat_history(sender_email: str, recipient_email: str):
    chat_history = conversation_collection.find({
        "$and": [
            {
                "$or": [
                    {"sender_email": sender_email, "recipient_email": recipient_email},
                    {"sender_email": recipient_email, "recipient_email": sender_email}
                ]
            }
        ]
    })
    chats = list(chat_history)
    print(chats)
    formatted_chats = [
        {
            "sender_email": chat["sender_email"],
            "recipient_email": chat["recipient_email"],
            "content": chat["content"],
        }
        for chat in chats
    ]
    print(formatted_chats)
    return formatted_chats
    
    