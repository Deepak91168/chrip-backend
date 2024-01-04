from models.user import User, LoginUser
from db.connectMongo import user_collection
from fastapi import APIRouter,Depends, HTTPException, Response, Request
from utils.security.security import hash_password, verify_password
from utils.auth.token import create_access_token, decode_token
from middlewares.auth.isAuthenticated import isAuthenticated
from datetime import datetime, timedelta
from schema.google_auth import GoogleLoginRequestUser

authRoute = APIRouter()

@authRoute.post("/auth/sign-up")
async def create_user(user: User):
    user_dict = user.dict()
    if(user_collection.find_one({"email": user_dict["email"]})):
        return HTTPException(status_code=400, detail="Email already exists")
    else:
        user_dict["password"] = hash_password(user_dict["password"])
        user_dict_without_password = {key: value for key, value in user_dict.items() if key != "password"}
        result = user_collection.insert_one(user_dict)
        return {"User created with id": str(user_dict_without_password)}

@authRoute.post("/auth/login")
async def login_user(response: Response,user: LoginUser):
    user_dict = user.dict()
    user_in_db = user_collection.find_one({"email": str(user_dict["email"])})
    if user_in_db:
        if verify_password(user_dict["password"], user_in_db["password"]):
            access_token = create_access_token(user_dict["email"])
            response.set_cookie(key="access_token", value=access_token, max_age=30*24*60*60, httponly=True)
            print(user_in_db)
            user_in_db.pop("password")
            if "_id" in user_in_db and isinstance(user_in_db["_id"], ObjectId):
                user_in_db["_id"] = str(user_in_db["_id"])
            currentUser = user_in_db
            return currentUser
        else:
            return HTTPException(status_code=400, detail="Incorrect password")
    else:
        return HTTPException(status_code=400, detail="Email not found")

@authRoute.post("/continue-with-google")
async def continue_with_google(request: Request, response: Response,user: GoogleLoginRequestUser):
    user_dict = user.dict()
    print(user_dict)
    user_in_db = user_collection.find_one({"email": str(user_dict["email"])})
    if(user_in_db is None):
        user_dict["password"] = hash_password(user_dict["email"])
        user_dict_without_password = {key: value for key, value in user_dict.items() if key != "password"}
        result = user_collection.insert_one(user_dict)
        access_token = create_access_token(user_dict["email"])
        response.set_cookie(key="access_token", value=access_token, max_age=30*24*60*60, httponly=True)
        print("Created new user")
        return {"access_token": access_token, "user": user_dict_without_password}
    else:
        user_dict_without_password = {key: value for key, value in user_dict.items() if key != "password"}
        access_token = create_access_token(user_dict["email"])
        response.set_cookie(key="access_token", value=access_token, max_age=30*24*60*60, httponly=True)
        return {"access_token": access_token, "user": user_dict_without_password}
    

@authRoute.get("/get-all-users", dependencies=[Depends(isAuthenticated)])
async def get_all_users():
    print("executing get_all_users")
    users = []
    for user in user_collection.find():
        users.append(User(**user))
    return users