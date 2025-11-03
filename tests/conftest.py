import os
import sys

app_dir = os.path.join(os.path.dirname(__file__),"..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from models import Base,Item
from sqlalchemy.orm import Session,sessionmaker

@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url= "sqlite://",
        connect_args={"check_same_thread":False},
        poolclass= StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
    db = SessionLocal()

    try:
        item1 = Item(name="tanaka",email="ahot@com")
        item2 = Item(name="yamada",email="wj3r@com")
        db.add(item1)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client_fixture(session_fixture :Session):
    def over_ride_get_db():
        return session_fixture
    
    app.dependency_overrides[get_db] = over_ride_get_db
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
