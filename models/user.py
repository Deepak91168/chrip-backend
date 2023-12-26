# models/user.py
from pydantic import BaseModel
from typing import List
class User(BaseModel):
    name: str
    email: str = None
    password: str
    contacts: List[str] = []
