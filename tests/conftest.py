from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from app import models
from alembic import command
from app.oauth2 import create_access_token

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

@pytest.fixture() #scope="module"
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
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


@pytest.fixture
def test_user(client):
    user_data = {"email":"kasun@gmail.com", "password":"12345"}
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email":"janitha@gmail.com", "password":"12345"}
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_user, session, test_user2):
    posts_data = [
        {
            "title":"first post",
            "content":"first content",
            "owner_id":test_user['id']
        },
        {
            "title": "second post",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "third post",
            "content": "third content",
            "owner_id": test_user['id']
        },
        {
            "title": "third post",
            "content": "third content",
            "owner_id": test_user2['id']
        }
    ]
    def creat_post_model(post):
        return models.Post(**post)

    post_map = map(creat_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts