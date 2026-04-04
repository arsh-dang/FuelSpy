from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from database import Base

    
class Stations(Base):
    __tablename__ =  "stations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    
    prices: Mapped[list["Prices"]] = relationship("Prices", back_populates="station")
    
class FuelTypes(Base):
    __tablename__ = "fuel_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
class Prices(Base):
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    price_cents: Mapped[float] = mapped_column(Float, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    station: Mapped["Stations"] = relationship("Stations", back_populates="prices")
    
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    price_cents: Mapped[float] = mapped_column(Float, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)