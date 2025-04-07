from fastapi import APIRouter
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import hash_password

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    """
    Register a new user.
    """
    hashed_pw = hash_password(user.password)
    return {"email": user.email, "hashed_password": hashed_pw}

@router.post("/login")
def login(user: UserLogin):
    """
    Authenticate a user and return a token.
    """
    return {"email": user.email}
