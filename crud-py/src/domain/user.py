from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    age: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
