from pydantic import BaseModel
from pydantic import EmailStr

class User(BaseModel):
    username        : str
    email           : EmailStr
    password        : str

class PublicUser(BaseModel):
    username        : str
    email           : EmailStr
    
class UserLogin(BaseModel):
    email           : EmailStr
    password        : str
    stay_logged     : bool


class Expense(BaseModel):
    description     : str
    value           : float
    date            : str
    category        : str
    category_color  : str

class Installment(BaseModel):
    description     : str
    category        : str
    category_color  : str
    quantity        : int
    inst_value      : float
    init_date       : str
    