from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Request schema for user registration.
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Request schema for user login.
    """
    email: EmailStr
    password: str
