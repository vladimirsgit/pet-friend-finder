

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlmodel import SQLModel

from app.core.config import Config

DATABASE_URL = f"postgresql+asyncpg://{Config.DATABASE_USERNAME}:{Config.DATABASE_PASSWORD}@{Config.DATABASE_HOST}:{Config.DATABASE_PORT}/{Config.DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,

)
async def init_db():
    async with engine.begin() as conn:
         await conn.execute(text("SELECT 1"))


async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session
