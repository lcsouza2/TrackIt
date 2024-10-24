from pydantic import BaseModel
from pydantic import EmailStr

class User(BaseModel):
    username : str
    email : EmailStr
    password : str

class PublicUser(BaseModel):
    username: str
    email: EmailStr
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    stay_logged : bool
