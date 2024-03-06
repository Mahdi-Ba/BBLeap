from core.db import get_db, Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from customers.models.customers_models import Base
from core.settings import settings

engine = create_engine(settings.DATABASE_TEST_URL, poolclass=StaticPool, )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_fixture():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


from main import app
from fastapi.testclient import TestClient

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
