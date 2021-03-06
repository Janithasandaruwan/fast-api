from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

# Establish the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Talk to the sql database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# When we get a request, it create session to send sql statements. After request is done, then it close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Make connection to the postgresSQL*************************************************************************************
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfully")
#         break
#     except Exception as error:
#         print("Error Connection")
#         print(error)
#         time.sleep(2)