import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.storage.main import StorageManager
from backend.core.contracts import RunResult, Classification, Scores
from backend.storage.models import Base

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Pytest fixture to create a new database session for each test function.
    Uses an in-memory SQLite database to ensure test isolation.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def storage_manager(db_session):
    """
    Pytest fixture that provides a `StorageManager` instance initialized
    with the test database session.
    """
    manager = StorageManager()
    manager.db = db_session
    return manager

def test_save_and_get_run(storage_manager):
    """
    Tests the core functionality of the StorageManager: saving a `RunResult`
    to the database and then retrieving it by its `run_id`.
    """
    run_data = {
        "case_id": "injection-001",
        "suite_id": "injection",
        "run_id": "run-123",
        "model_id": "gpt-4-turbo",
        "timestamp_utc": datetime.now(),
        "classification": {"primary": "pass"},
        "scores": {"accuracy": 1.0}
    }
    run_result = RunResult(**run_data)
    
    # Action: Save the run result
    storage_manager.save_run(run_result)
    
    # Action: Retrieve the run result
    retrieved_run = storage_manager.get_run("run-123")
    
    # Assert: Check that the retrieved data matches the original data
    assert retrieved_run is not None
    assert retrieved_run.run_id == "run-123"
    assert retrieved_run.case_id == "injection-001"
    assert retrieved_run.classification["primary"] == "pass"