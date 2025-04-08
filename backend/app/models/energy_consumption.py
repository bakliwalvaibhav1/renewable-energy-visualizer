from sqlalchemy import Column, String, Float, DateTime
from app.models.base import Base


class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    energy_kwh = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    consumer_id = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
