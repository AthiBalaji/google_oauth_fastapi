from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_database_url

DATABASE_URL = get_database_url()

# Create async engine (connection pool managed internally)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,               # set True for debugging
    pool_pre_ping=True,       # checks stale connections
    pool_size=5,              # base connections
    max_overflow=10,          # extra connections
)

# Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency (IMPORTANT)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()