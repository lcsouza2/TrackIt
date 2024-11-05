from typing import Literal, Optional
from pydantic import BaseModel
from pydantic import EmailStr

class User(BaseModel):
    username            : str
    email               : EmailStr
    password            : str

class PublicUser(BaseModel):
    username            : str
    email               : EmailStr
    
class UserLogin(BaseModel):
    email               : EmailStr
    password            : str
    stay_logged         : bool

class Expense(BaseModel):
    description         : str
    value               : float
    date                : str
    category            : str

class ExpenseEdit(Expense):
    id                  : int
    
class DeleteSpent(BaseModel):
    type                : Literal["Expense",  "Installment"]
    id                  : int

class Installment(BaseModel):
    description         : str
    category            : str
    quantity            : int
    installment_value   : float
    init_date           : str
    interests           : Optional[float | int]

class Category(BaseModel):
    name                : str
    color               : str

class Filters(BaseModel):
    expense_types       : list
    expense_date        : dict
    expense_categories  : list
    expense_values       : dict