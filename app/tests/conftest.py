import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.main import app
from fastapi.testclient import TestClient
from app.config import settings

# Create a database engine for the test database
engine = create_engine(settings.TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.create_all(bind=engine)  # Create tables for tests
    yield
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests

@pytest.fixture(scope="function")
def client(setup_db):
    with TestClient(app) as c:
        yield c
