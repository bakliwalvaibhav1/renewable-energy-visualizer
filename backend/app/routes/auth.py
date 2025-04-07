from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    """
    Register a new user.
    """
    return {"message": "Register endpoint"}

@router.post("/login")
def login():
    """
    Authenticate a user and return a token.
    """
    return {"message": "Login endpoint"}
