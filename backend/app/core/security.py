from datetime import UTC, datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import config
from app.core.logger import setup_logger

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
logger = setup_logger(__name__)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    logger.info("🔒 Hashing password...")
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password using bcrypt.

    Args:
        plain_password (str): Plain password input.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    logger.info("🔍 Verifying password...")
    valid = bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
    if valid:
        logger.info("✅ Password verified successfully.")
    else:
        logger.warning("❌ Password verification failed.")
    return valid


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JSON Web Token (JWT) containing user data and expiration time.

    Args:
        data (dict): Data to include in the token.
        expires_delta (timedelta, optional): Token lifetime.

    Returns:
        str: Encoded JWT token.
    """
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"🔑 Created access token, expires at {expire.isoformat()}")
    return token


def decode_access_token(token: str) -> dict | None:
    """
    Decode and verify a JWT token.

    Args:
        token (str): The encoded JWT token.

    Returns:
        dict | None: Decoded payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info("✅ Token successfully decoded.")
        return payload
    except JWTError as e:
        logger.warning(f"⚠️ Token decoding failed: {str(e)}")
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Extract and validate a JWT access token from the request header.

    Args:
        token (str): The bearer token from the request.

    Raises:
        HTTPException: If token is invalid or expired.

    Returns:
        dict: Decoded JWT payload.
    """
    logger.info("👤 Getting current user from token...")
    payload = decode_access_token(token)
    if payload is None:
        logger.warning("❌ Invalid or expired token received.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    logger.info(f"✅ Authenticated user: {payload.get('sub')}")
    return payload
