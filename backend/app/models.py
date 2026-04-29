from sqlalchemy import Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.database import Base

    
class Stations(Base):
    __tablename__ =  "stations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    
    prices: Mapped[list["Prices"]] = relationship("Prices", back_populates="station")
    price_history: Mapped[list["PriceHistory"]] = relationship("PriceHistory", back_populates="station")
    
class FuelTypes(Base):
    __tablename__ = "fuel_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    prices: Mapped[list["Prices"]] = relationship("Prices", back_populates="fuel_type")
    price_history: Mapped[list["PriceHistory"]] = relationship("PriceHistory", back_populates="fuel_type")
    
class Prices(Base):
    __tablename__ = "prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    price_cents: Mapped[float] = mapped_column(Float, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    isAvailable: Mapped[bool] = mapped_column(Boolean, name="isAvailable", nullable=False)    
    
    station: Mapped["Stations"] = relationship("Stations", back_populates="prices")
    fuel_type: Mapped["FuelTypes"] = relationship("FuelTypes", back_populates="prices")
    
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    station_id: Mapped[int] = mapped_column(Integer, ForeignKey("stations.id"), nullable=False)
    fuel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    price_cents: Mapped[float] = mapped_column(Float, nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    station: Mapped["Stations"] = relationship("Stations", back_populates="price_history")
    fuel_type: Mapped["FuelTypes"] = relationship("FuelTypes", back_populates="price_history")