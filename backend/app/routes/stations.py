from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from typing import Annotated

from app import schemas, models
from app.database import get_session


app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "FuelSpy API"}

@app.get("/api/stations/", response_model=list[schemas.StationListResponse])
async def stations_data(fuel_type: str | None = None,
                        sort: str | None = None,
                        latitude: float | None = None,
                        longitude: float | None = None,
                        session: Annotated[AsyncSession, Depends(get_session)] = None):
    query = select(models.Stations)

    needs_price_join = sort is not None

    # Filter which stations (always when fuel_type set)
    if fuel_type is not None:
        stations_ids = select(models.Prices.station_id).join(models.FuelTypes).where(
            models.FuelTypes.name == fuel_type
        )
        query = query.where(models.Stations.id.in_(stations_ids))


    # Join for sorting (only when sort is set)
    if needs_price_join:
        if fuel_type is not None:
            query = query.join(models.Prices).join(models.FuelTypes).where(
                models.FuelTypes.name == fuel_type
            )
        else:
            query = query.join(models.Prices)
        query = query.group_by(models.Stations.id)
        
    # Eager load prices while the session is open, lazy loading loads the prices when the session is off (creating an error)
    if fuel_type is not None:
        ft_subquery = select(models.FuelTypes.id).where(models.FuelTypes.name == fuel_type)
        query = query.options(
            selectinload(models.Stations.prices.and_(models.Prices.fuel_type_id.in_(ft_subquery)))
            .selectinload(models.Prices.fuel_type)
        ) 
    else:
        query = query.options(
            selectinload(models.Stations.prices).selectinload(models.Prices.fuel_type)
        )

    if sort == "price_asc":
        query = query.order_by(func.min(models.Prices.price_cents))
    elif sort == "price_desc":
        query = query.order_by(func.min(models.Prices.price_cents).desc())


    results = await session.execute(query)
    stations = results.scalars().all()

    return stations if stations else []

@app.get("/api/stations/{id}",
    response_model=schemas.StationDetailResponse,
    responses={404: {"description": "Station not found"}},
)
async def station_data_id(id: int,
                          session: Annotated[AsyncSession, Depends(get_session)]):

    query = select(models.Stations).options(
        selectinload(models.Stations.prices).selectinload(models.Prices.fuel_type)
    ).where(models.Stations.id == id)
    result = await session.execute(query)
    station = result.scalar_one_or_none()

    if not station:
        raise HTTPException(status_code=404, detail="Station not found")

    return station

@app.get(
    "/api/stations/{id}/history",
    response_model=list[schemas.PriceHistoryResponse],
    responses={404: {"description": "Station not found"}},
)
async def station_data_history(id: int, days: int = 7,
                               session: Annotated[AsyncSession, Depends(get_session)] = None):
    cutoff = datetime.now() - timedelta(days=days)
    query = select(models.PriceHistory).options(
        selectinload(models.PriceHistory.fuel_type)
    ).where(
        and_(
            models.PriceHistory.station_id == id,
            models.PriceHistory.fetched_at >= cutoff
        )
    )

    result = await session.execute(query)
    history = result.scalars().all()

    if not history:
        raise HTTPException(status_code=404, detail="Station not found")

    return history
