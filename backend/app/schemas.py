from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Fuel Type response
class FuelTypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str

# Current price for a station
class PriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fuel_type_id: int
    fuel_type: FuelTypeResponse
    price_cents: float
    fetched_at: datetime

# Station in list (with all current prices)
class StationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    brand: str
    prices: list[PriceResponse]

# Station detail (same as list for now)
class StationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    brand: str
    prices: list[PriceResponse]

# Price history record
class PriceHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    station_id: int
    fuel_type_id: int
    fuel_type: FuelTypeResponse
    price_cents: float
    fetched_at: datetime