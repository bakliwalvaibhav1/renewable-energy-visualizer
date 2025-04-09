import asyncio
import csv
import os
from datetime import datetime

from sqlalchemy.future import select

from app.core.database import AsyncSessionLocal, engine
from app.core.logger import setup_logger
from app.core.security import hash_password
from app.models.base import Base
from app.models.user import User
from app.models.energy_generation import EnergyGeneration
from app.models.energy_consumption import EnergyConsumption

logger = setup_logger(__name__)

DATA_DIR = "data"
GEN_CSV = os.path.join(DATA_DIR, "energy_generation.csv")
CONSUMPTION_CSV = os.path.join(DATA_DIR, "energy_consumption.csv")


async def init_models():
    """
    Initializes database tables, creates demo user,
    and inserts energy data from CSVs.
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

        # ⚡ Insert energy generation data
        gen_result = await session.execute(select(EnergyGeneration).limit(1))
        gen_exists = gen_result.scalar_one_or_none()

        if not gen_exists and os.path.exists(GEN_CSV):
            logger.info(f"📥 Loading energy generation data from '{GEN_CSV}'...")
            with open(GEN_CSV, newline="") as f:
                reader = csv.DictReader(f)
                gen_entries = [
                    EnergyGeneration(
                        id=row["id"],
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        energy_kwh=float(row["energy_kwh"]),
                        source=row["source"],
                        location=row["location"],
                        system_id=row["system_id"],
                    )
                    for row in reader
                ]
            session.add_all(gen_entries)
            await session.commit()
            logger.info(f"✅ Inserted {len(gen_entries)} energy generation rows.")
        elif gen_exists:
            logger.info("ℹ️ Energy generation data already exists. Skipping CSV import.")
        else:
            logger.warning(f"⚠️ Generation CSV not found at '{GEN_CSV}'.")

        # 🔌 Insert energy consumption data
        cons_result = await session.execute(select(EnergyConsumption).limit(1))
        cons_exists = cons_result.scalar_one_or_none()

        if not cons_exists and os.path.exists(CONSUMPTION_CSV):
            logger.info(f"📥 Loading energy consumption data from '{CONSUMPTION_CSV}'...")
            with open(CONSUMPTION_CSV, newline="") as f:
                reader = csv.DictReader(f)
                consumption_entries = [
                    EnergyConsumption(
                        id=row["id"],
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        energy_kwh=float(row["energy_kwh"]),
                        location=row["location"],
                        sector=row["sector"],
                        consumer_id=row["consumer_id"],
                        price=float(row["price"]),
                        total=float(row["total"]),
                    )
                    for row in reader
                ]
            session.add_all(consumption_entries)
            await session.commit()
            logger.info(f"✅ Inserted {len(consumption_entries)} energy consumption rows.")
        elif cons_exists:
            logger.info("ℹ️ Energy consumption data already exists. Skipping CSV import.")
        else:
            logger.warning(f"⚠️ Consumption CSV not found at '{CONSUMPTION_CSV}'.")


if __name__ == "__main__":
    asyncio.run(init_models())
