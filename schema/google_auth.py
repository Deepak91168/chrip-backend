from pydantic import BaseModel

class GoogleLoginRequestUser(BaseModel):
    name:str = None
    email:str = None