from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from raspberries.adapters.config import settings

engine = create_async_engine(settings.postgres_url)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
