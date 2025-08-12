"""
Provides a high-level interface for interacting with the database storage.

This module defines the `StorageManager` class, which encapsulates all database
operations, such as saving and retrieving test run results. It abstracts the
underlying database implementation (SQLAlchemy ORM) and provides simple,
application-specific methods.
"""
from sqlalchemy.orm import Session
from . import models, database
from ..core.contracts import RunResult


class StorageManager:
    """Manages all interactions with the SQLite database."""

    def __init__(self):
        """
        Initializes the StorageManager by creating a new database session.
        """
        self.db: Session = database.SessionLocal()

    def save_run(self, run: RunResult) -> models.RunResultDB:
        """
        Saves a single test run result to the database.

        Args:
            run: A `RunResult` object containing the data to be saved.

        Returns:
            The database object that was created.
        """
        # Only pass fields that the database model expects
        db_data = {}
        run_data = run.model_dump()
        db_fields = ['run_id', 'case_id', 'suite_id', 'model_id', 'timestamp_utc', 
                     'raw_response', 'error', 'classification', 'scores']
        
        for field in db_fields:
            if field in run_data and run_data[field] is not None:
                db_data[field] = run_data[field]
        
        run_db = models.RunResultDB(**db_data)
        self.db.add(run_db)
        self.db.commit()
        self.db.refresh(run_db)
        return run_db

    def get_run(self, run_id: str) -> models.RunResultDB | None:
        """
        Retrieves a single test run result from the database by its ID.

        Args:
            run_id: The unique identifier of the test run.

        Returns:
            The `RunResultDB` object if found, otherwise None.
        """
        return self.db.query(models.RunResultDB).filter(
            models.RunResultDB.run_id == run_id
        ).first()


def create_tables():
    """
    Creates all necessary database tables based on the defined ORM models.

    This function should be called once at application startup to ensure the
    database schema is correctly initialized.
    """
    models.Base.metadata.create_all(bind=database.engine)