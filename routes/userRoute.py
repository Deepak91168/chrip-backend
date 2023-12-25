from models.user import User
from db.connectMongo import collection
from fastapi import APIRouter,Depends, HTTPException, Response
from utils.security.security import hash_password, verify_password
from utils.auth.token import create_access_token, decode_token
from middlewares.auth.isAuthenticated import isAuthenticated
from datetime import datetime, timedelta

userRoute = APIRouter()

@userRoute.post("/sign-up")
async def create_user(user: User):
    user_dict = user.dict()
    if(collection.find_one({"email": user_dict["email"]})):
        return HTTPException(status_code=400, detail="Email already exists")
    else:
        user_dict["password"] = hash_password(user_dict["password"])
        user_dict_without_password = {key: value for key, value in user_dict.items() if key != "password"}
        result = collection.insert_one(user_dict)
        return {"User created with id": str(user_dict_without_password)}

@userRoute.post("/login")
async def login_user(response: Response,user: User):
    user_dict = user.dict()
    user_in_db = collection.find_one({"email": str(user_dict["email"])})
    if user_in_db:
        if verify_password(user_dict["password"], user_in_db["password"]):
            access_token = create_access_token(user_dict["email"])
            response.set_cookie(key="access_token", value=access_token, max_age=30*24*60*60, httponly=True)
            return {"access_token": access_token}
        else:
            return HTTPException(status_code=400, detail="Incorrect password")
    else:
        return HTTPException(status_code=400, detail="Email not found")


@userRoute.get("/get-all-users", dependencies=[Depends(isAuthenticated)])
async def get_all_users():
    print("executing get_all_users")
    users = []
    for user in collection.find():
        users.append(User(**user))
    return users