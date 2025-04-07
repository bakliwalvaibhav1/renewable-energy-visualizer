from fastapi import APIRouter
from app.schemas.auth import UserRegister, UserLogin

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    """
    Register a new user.
    """
    return {"email": user.email}

@router.post("/login")
def login(user: UserLogin):
    """
    Authenticate a user and return a token.
    """
    return {"email": user.email}
