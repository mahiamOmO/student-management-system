from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "student"

class UserResponse(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    uap_id: str
    name: str
    department: str
    batch: str
    user_id: int

class StudentResponse(BaseModel):
    id: int
    uap_id: str
    name: str
    class Config:
        from_attributes = True