from fastapi import APIRouter, Depends
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import hash_password, create_access_token, get_current_user

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

@router.get("/me")
def read_profile(user: dict = Depends(get_current_user)):
    """
    Returns the current authenticated user's profile info.

    Args:
        user (dict): The user data extracted from the token payload.

    Returns:
        dict: User info (currently only email).
    """
    return {"email": user["sub"]}