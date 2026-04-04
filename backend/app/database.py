from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "fuelspy"
    
    class Config:
        env_file = "../../.env"
    
    @property
    def database_url(self) -> str:
        password = quote_plus(self.db_password)
        return f"postgresql+asyncpg://{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
    )

class Base(DeclarativeBase):
    pass