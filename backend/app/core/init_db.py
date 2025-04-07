import asyncio
from app.core.database import engine, AsyncSessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.models.base import Base

from sqlalchemy.future import select

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        demo_email = "demo@example.com"
        demo_password = "demopass"

        # 🔍 Get or create the demo user
        result = await session.execute(select(User).where(User.email == demo_email))
        demo_user = result.scalar_one_or_none()

        if not demo_user:
            demo_user = User(
                email=demo_email,
                hashed_password=hash_password(demo_password)
            )
            session.add(demo_user)
            await session.commit()
            await session.refresh(demo_user)
        else:
            print("User already exists")

if __name__ == "__main__":
    asyncio.run(init_models())
