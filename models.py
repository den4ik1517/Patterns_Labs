from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    userId: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)

class AppCreate(BaseModel):
    appId: str = Field(..., max_length=50)
    appName: str = Field(..., max_length=255)
    description: str
    category: str = Field(..., max_length=100)
    version: str = Field(..., max_length=20)
    size: float
