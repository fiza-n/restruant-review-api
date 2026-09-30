import os 


os.environ["DATABASE_URL"] = (
    ""
)



import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base, get_db
from main import app
from sqlalchemy.pool import NullPool




@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        os.environ["DATABASE_URL"],
        poolclass=NullPool
    )
    return engine

@pytest.fixture(scope="session")
def setup_database(test_engine):

    Base.metadata.create_all(bind=test_engine)
    
    yield
    
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

@pytest.fixture(scope="session")
def db_session(test_engine, setup_database):
    conn = test_engine.connect()
    trans = conn.begin()

    test_session = sessionmaker(bind=conn,expire_on_commit=False, join_transaction_mode="create_savepoint")

    with test_session as session:
        try: 
           yield session

        finally: 
            session.close()
            session.rollback()
            conn.close()
