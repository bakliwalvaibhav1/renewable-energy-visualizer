from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.energy_generation import EnergyGeneration
from app.models.energy_consumption import EnergyConsumption
from app.schemas.energy import EnergyGenerationRead, EnergyConsumptionRead
from app.core.database import get_db
from app.core.logger import setup_logger

from app.core.security import get_current_user

router = APIRouter()
logger = setup_logger(__name__)


@router.get("/generation", response_model=List[EnergyGenerationRead])
async def get_all_generation(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Returns all energy generation records.
    """
    logger.info("📡 Fetching energy generation data...")
    result = await db.execute(select(EnergyGeneration))
    records = result.scalars().all()
    logger.info(f"✅ {len(records)} generation records retrieved.")
    return records


@router.get("/consumption", response_model=List[EnergyConsumptionRead])
async def get_all_consumption(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Returns all energy consumption records.
    """
    logger.info("📡 Fetching energy consumption data...")
    result = await db.execute(select(EnergyConsumption))
    records = result.scalars().all()
    logger.info(f"✅ {len(records)} consumption records retrieved.")
    return records
