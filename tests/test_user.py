from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from alembic import command

#CREATE THE TEST DATABASE INSTEAD OF ORIGINAL DATABASE******************************************************************
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

# Establish the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Talk to the sql database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# When we get a request, it create session to send sql statements. After request is done, then it close it
# def overeide_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# app.dependency_overrides[get_db] = overeide_get_db
#***********************************************************************************************************************

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Run our code before we return our test
    #command.downgrade("base")
    #command.upgrade("head")
    def overeide_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overeide_get_db
    yield TestClient(app)
    # Run our code after our test finishes



def test_root(client):
    res = client.get("/")
    #print(res.json().get('message'))
    assert res.json().get('message') == 'Hellow FastAPI!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email" : "janitha@gmail.com", "password" : "12345"})
    #print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "janitha@gmail.com"
    assert res.status_code == 201