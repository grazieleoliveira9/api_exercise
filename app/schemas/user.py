from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = False
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    name: str
    email: str
    age: int
    city: str

class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()


class UserResponse(UserBase):
    id: int

class UserRequest(UserBase):
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None

class UserResponseUser(UserBase):
    name: str
    email: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None


