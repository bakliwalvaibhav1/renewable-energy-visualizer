from sqlalchemy import Column, Integer, String

from app.models.base import Base


class User(Base):
    """
    SQLAlchemy model for a registered user.

    Attributes:
        id (int): Primary key
        email (str): Unique user email
        hashed_password (str): Hashed password
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
