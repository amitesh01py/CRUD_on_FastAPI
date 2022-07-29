import uuid
from pydantic import BaseModel
from typing import List
import datetime
import email
import imp


class Addsong(BaseModel):
    song_name: str


#admin registration
class UserAdmin(BaseModel):
    full_name : str
    e_mail : str
    phone_number:str
    password : str

class UserLogin(BaseModel):
    e_mail : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"

class UpdateAdmin(BaseModel):
    id : uuid.UUID
    full_name : str
    e_mail : str
    phone_number:str 

class DeleteAdmin(BaseModel):
    id : uuid.UUID      
    



