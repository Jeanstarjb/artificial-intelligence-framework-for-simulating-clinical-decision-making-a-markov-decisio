import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/testdb"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def session(test_db):
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = lambda: TestSessionLocal()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()