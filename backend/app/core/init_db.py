import asyncio
from sqlalchemy.future import select

from app.core.database import engine, AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.models.base import Base
from app.core.logger import setup_logger

logger = setup_logger(__name__)

async def init_models():
    """
    Initializes database tables and creates a demo user if not present.
    """
    logger.info("📦 Starting database table creation...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tables created successfully.")

    async with AsyncSessionLocal() as session:
        demo_email = "demo@example.com"
        demo_password = "demopass"

        logger.info(f"🔍 Checking for existing demo user: {demo_email}")
        result = await session.execute(select(User).where(User.email == demo_email))
        demo_user = result.scalar_one_or_none()

        if not demo_user:
            logger.info("👤 Creating new demo user...")
            demo_user = User(
                email=demo_email,
                hashed_password=hash_password(demo_password)
            )
            session.add(demo_user)
            await session.commit()
            await session.refresh(demo_user)
            logger.info(f"✅ Demo user created: {demo_user.email}")
        else:
            logger.info("ℹ️ Demo user already exists. Skipping creation.")

if __name__ == "__main__":
    asyncio.run(init_models())
