from pydantic import BaseModel
from datetime import datetime


class EnergyGenerationBase(BaseModel):
    timestamp: datetime
    energy_kwh: float
    source: str
    location: str
    system_id: str


class EnergyGenerationCreate(EnergyGenerationBase):
    pass


class EnergyGenerationRead(EnergyGenerationBase):
    id: str

    class Config:
        orm_mode = True


class EnergyConsumptionBase(BaseModel):
    timestamp: datetime
    energy_kwh: float
    location: str
    sector: str
    consumer_id: str
    price: float
    total: float


class EnergyConsumptionCreate(EnergyConsumptionBase):
    pass


class EnergyConsumptionRead(EnergyConsumptionBase):
    id: str

    class Config:
        orm_mode = True
