from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional, List

# Role Enum for input validation
class Role(str, Enum):
    client = "client"
    ops = "ops"

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    is_verified: bool

    class Config:
        orm_mode = True

# File Upload Response
class FileOut(BaseModel):
    id: int
    filename: str
    uploader_id: int

    class Config:
        orm_mode = True

# Download Link Response
class DownloadLink(BaseModel):
    download_link: str
    message: str = "success"

# JWT Token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[Role] = None
