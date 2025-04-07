from fastapi import APIRouter
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import hash_password, create_access_token

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
    Authenticate a user and return a JWT token.
    """
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}