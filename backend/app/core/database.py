from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import config
from app.models import Base

metadata = Base.metadata

# Create async SQLAlchemy engine
engine = create_async_engine(config.DATABASE_URL, echo=config.SQLALCHEMY_ECHO)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    """
    Dependency that provides an async DB session.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async with AsyncSessionLocal() as session:
        yield session
