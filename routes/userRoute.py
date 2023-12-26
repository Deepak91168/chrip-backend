from models.user import User
from db.connectMongo import user_collection
from fastapi import APIRouter,Depends, HTTPException, Response, Request
from utils.security.security import hash_password, verify_password
from utils.auth.token import create_access_token, decode_token
from middlewares.auth.isAuthenticated import isAuthenticated
from datetime import datetime, timedelta
from schema.google_auth import GoogleLoginRequestUser

userRoute = APIRouter()

@userRoute.put("/user/add-friend/{friend_email}", dependencies=[Depends(isAuthenticated)])
async def add_friend_to_contacts(friend_email: str, request: Request):
    access_token = request.cookies.get("access_token")
    if access_token:
        decoded = decode_token(access_token)
        user_email = decoded["sub"]
        user = user_collection.find_one({"email": user_email})
        print(user)
        if user:
            if friend_email in user["contacts"]:
                return HTTPException(status_code=400, detail="Friend already exists")
            else:
                user_collection.update_one({"email": user_email}, {"$push": {"contacts": friend_email}})
                return {"message": "Friend added successfully"}
        else:
            return HTTPException(status_code=400, detail="User not found")
    else:
        return HTTPException(status_code=401, detail="Not authenticated")
    
