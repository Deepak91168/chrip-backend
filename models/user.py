# models/user.py
from pydantic import BaseModel
from typing import List
class User(BaseModel):
    name: str = None
    email: str
    password: str
    contacts: List[str] = []
    
class LoginUser(BaseModel):
    email: str
    password: str
