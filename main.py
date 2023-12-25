from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from models.user import User
from db.connectMongo import collection
from routes.authRoute import authRoute
app = FastAPI()

app.include_router(authRoute)



