from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.database import get_db
from app.core.logger import setup_logger

router = APIRouter(tags=["Auth"])
logger = setup_logger(__name__)

@router.post("/register", status_code=201)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user in the database after hashing their password.

    Args:
        user (UserCreate): Incoming registration data (email and password).
        db (AsyncSession): Injected SQLAlchemy session.

    Raises:
        HTTPException: If a user with the same email already exists.

    Returns:
        dict: Success message and the registered user's email.
    """
    logger.info(f"Attempting to register user: {user.email}")
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        logger.warning(f"Registration failed: Email already registered - {user.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"User registered successfully: {new_user.email}")
    return {"message": "User registered successfully", "email": new_user.email}


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates a user by verifying their email and password from the database.

    Args:
        form_data (OAuth2PasswordRequestForm): The incoming login form with username (email) and password.
        db (AsyncSession): Injected SQLAlchemy session.

    Raises:
        HTTPException: If credentials are invalid.

    Returns:
        dict: JWT access token and token type.
    """
    logger.info(f"Login attempt for user: {form_data.username}")
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Invalid credentials for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.email})
    logger.info(f"Login successful: {user.email}")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def read_profile(user: dict = Depends(get_current_user)):
    """
    Returns the current authenticated user's profile info.

    Args:
        user (dict): The user data extracted from the token payload.

    Returns:
        dict: User info (currently only email).
    """
    logger.info(f"Profile accessed: {user['sub']}")
    return {"email": user["sub"]}


@router.get("/dashboard")
def get_dashboard(user: dict = Depends(get_current_user)):
    """
    Simulated protected route that requires JWT authentication.

    Args:
        user (dict): Decoded JWT payload injected by get_current_user

    Returns:
        dict: Personalized message
    """
    logger.info(f"Dashboard accessed by: {user['sub']}")
    return {"message": f"Welcome back, {user['sub']}! You are viewing your dashboard."}
