from pydantic import BaseModel, EmailStr
from datetime import datetime
class Message(BaseModel):
    sender_email: str
    recipient_email: str
    content: str
    timestamp: datetime = datetime.now() 
    
