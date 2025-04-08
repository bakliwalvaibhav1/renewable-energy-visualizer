from sqlalchemy import Column, String, Float, DateTime
from app.models.base import Base


class EnergyGeneration(Base):
    __tablename__ = "energy_generation"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    energy_kwh = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    location = Column(String, nullable=False)
    system_id = Column(String, index=True, nullable=False)
