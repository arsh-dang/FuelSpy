import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, engine, Base
from app import models


async def seed_database():
    # Create all tables - using fuelspy_admin user which should have permissions
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully")
    except Exception as e:
        print(f"Table creation note: {e}")
        print("Proceeding with seeding (tables may already exist)...")
    
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        existing_stations = await session.execute(
            select(models.Stations).limit(1)
        )
        if existing_stations.scalars().first():
            print("Database already seeded. Skipping...")
            return
        
        # Create fuel types
        fuel_types = [
            models.FuelTypes(name="E10"),
            models.FuelTypes(name="U91"),
            models.FuelTypes(name="U95"),
            models.FuelTypes(name="U98"),
            models.FuelTypes(name="Diesel"),
        ]
        session.add_all(fuel_types)
        await session.flush()  # Flush to get IDs
        
        # Create 10 Geelong stations
        stations = [
            models.Stations(
                name="Shell Geelong",
                address="123 Main Street, Geelong VIC 3220",
                latitude=-38.1449,
                longitude=144.3615,
                brand="Shell"
            ),
            models.Stations(
                name="BP Geelong North",
                address="456 Malop Street, Geelong VIC 3220",
                latitude=-38.1350,
                longitude=144.3650,
                brand="BP"
            ),
            models.Stations(
                name="Caltex Geelong West",
                address="789 Western Avenue, Geelong VIC 3218",
                latitude=-38.1500,
                longitude=144.3400,
                brand="Caltex"
            ),
            models.Stations(
                name="Shell Newtown",
                address="321 Gheringhap Street, Geelong VIC 3220",
                latitude=-38.1320,
                longitude=144.3750,
                brand="Shell"
            ),
            models.Stations(
                name="BP Bellerine Street",
                address="654 Bellerine Street, Geelong VIC 3220",
                latitude=-38.1280,
                longitude=144.3780,
                brand="BP"
            ),
            models.Stations(
                name="Fuel Stop Manifold",
                address="111 Manifold Street, Geelong VIC 3220",
                latitude=-38.1550,
                longitude=144.3550,
                brand="Independent"
            ),
            models.Stations(
                name="Shell Highton",
                address="222 Highton Road, Highton VIC 3216",
                latitude=-38.1700,
                longitude=144.4000,
                brand="Shell"
            ),
            models.Stations(
                name="Mobil Waurn Ponds",
                address="333 Waurn Ponds Drive, Geelong VIC 3216",
                latitude=-38.1600,
                longitude=144.3900,
                brand="Mobil"
            ),
            models.Stations(
                name="Caltex Ceres Street",
                address="555 Ceres Street, Geelong VIC 3220",
                latitude=-38.1400,
                longitude=144.3550,
                brand="Caltex"
            ),
            models.Stations(
                name="BP Deakin",
                address="789 Bellarine Street, Geelong VIC 3220",
                latitude=-38.1200,
                longitude=144.3690,
                brand="BP"
            ),
        ]
        session.add_all(stations)
        await session.flush()
        
        # Create price records for each station
        price_data = [
            {"fuel_type": 0, "price": 14250},  # E10
            {"fuel_type": 1, "price": 16550},  # U91
            {"fuel_type": 2, "price": 17850},  # U95
            {"fuel_type": 3, "price": 19200},  # U98
            {"fuel_type": 4, "price": 17950},  # Diesel
        ]
        
        for station in stations:
            for price_info in price_data:
                price = models.Prices(
                    station_id=station.id,
                    fuel_type_id=price_info["fuel_type"] + 1,  # IDs start at 1
                    price_cents=price_info["price"],
                    fetched_at=datetime.now()
                )
                session.add(price)
                
                # Also add to history
                history = models.PriceHistory(
                    station_id=station.id,
                    fuel_type_id=price_info["fuel_type"] + 1,
                    price_cents=price_info["price"],
                    fetched_at=datetime.now()
                )
                session.add(history)
        
        await session.commit()
        print("Database seeded successfully with 10 Geelong stations!")


if __name__ == "__main__":
    asyncio.run(seed_database())
