from pydantic import BaseModel, EmailStr
from typing import Optional

class SigninRequest(BaseModel):
    username: str
    password: str



class SignupRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str



class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str



class UserWithPw(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str