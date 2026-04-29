import os
import uuid
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert

from app import models

BASE_URL = "https://api.fuel.service.vic.gov.au/open-data/v1"

def _headers(consumer_id: str) -> dict[str,str]:
    return {
        "x-consumer-id": consumer_id,
        "x-transactionid": str(uuid.uuid4()),
        "User-Agent": "FuelSpy/1.0",
    }
    
async def fetch_and_store_prices(session: AsyncSession) -> int:
    consumer_id = os.environ["FAIR_FUEL_CONSUMER_ID"]
    
    async with httpx.AsyncClient() as client:
        brands_resp = await client.get(
            f"{BASE_URL}/fuel/reference-data/brands",
            headers=_headers(consumer_id)
        )
        brands_resp.raise_for_status()
        brands_map = {b["id"]: b["name"] for b in brands_resp.json()["brands"]}
        
        prices_resp = await client.get(
            f"{BASE_URL}/fuel/prices",
            headers=_headers(consumer_id),
        )
        prices_resp.raise_for_status()
        details = prices_resp.json()["fuelPriceDetails"]
        
    # Cache fuel types by code to avoid repeated queries
    fuel_type_cache: dict[str, int] = {}
    
    for item in details:
        api_station = item["fuelStation"]
        external_id = api_station["id"]
        
        # Upsert station
        result = await session.execute(
            select(models.Stations).where(models.Stations.external_id == external_id)
        )
        
        station = result.scalar_one_or_none()
        
        brand_name = brands_map.get(api_station.get("brandId", ""), "Unknown")
        
        if station is None:
            station = models.Stations(
                external_id=external_id,
                name=api_station["name"],
                address=api_station["address"],
                latitude=api_station["location"]["latitude"],
                longitude=api_station["location"]["longitude"],
                brand=brand_name,
            )
            session.add(station)
            await session.flush() # get station.id
        else:
            station.name = api_station["name"]
            station.address = api_station["address"]
            station.latitude = api_station["location"]["latitude"]
            station.longitude = api_station["location"]["longitude"]
            station.brand = brand_name
            
        for fuel_price in item["fuelPrices"]:
            code = fuel_price["fuelType"]
            if fuel_price["price"] is None:
                continue
            price_value = round(fuel_price["price"] * 100)
            is_available = fuel_price["isAvailable"]


            # Find or create fuel type
            if code not in fuel_type_cache:
                ft_result = await session.execute(
                    select(models.FuelTypes).where(models.FuelTypes.name == code)
                )
                ft = ft_result.scalar_one_or_none()
                if ft is None:
                    ft = models.FuelTypes(name=code)
                    session.add(ft)
                    await session.flush()
                fuel_type_cache[code] = ft.id
                
            fuel_type_id = fuel_type_cache[code]
            
            # Replace current price
            await session.execute(
                delete(models.Prices).where(
                    models.Prices.station_id == station.id,
                    models.Prices.fuel_type_id == fuel_type_id,
                )
            )
            
            session.add(models.Prices(
                station_id=station.id,
                fuel_type_id=fuel_type_id,
                price_cents=price_value,
                isAvailable=is_available,
            ))
            
            # Append history
            session.add(models.PriceHistory(
                station_id=station.id,
                fuel_type_id=fuel_type_id,
                price_cents=price_value,
            ))
            
    await session.commit()
    return len(details)