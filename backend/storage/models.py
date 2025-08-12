"""
Defines the SQLAlchemy ORM models for the database.

This module contains the Python classes that map to the tables in the SQLite
database. SQLAlchemy's declarative base is used to define the table schema
in a Python-native way. Each class represents a table, and its attributes
represent the columns.
"""
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base

# The declarative base is a factory for creating new base classes for ORM models.
Base = declarative_base()


class RunResultDB(Base):
    """
    ORM model representing a single test case result in the database.

    This class maps to the `run_results` table and defines the schema for
    storing all information related to the execution of a single test case
    against a specific model.
    """
    __tablename__ = "run_results"

    # The unique identifier for the entire test run.
    run_id = Column(String, primary_key=True, index=True)
    # The ID of the TestCase that was run.
    case_id = Column(String, index=True)
    # The ID of the test suite this case belongs to.
    suite_id = Column(String, index=True)
    # The identifier of the model that was tested (e.g., 'gpt-4-turbo').
    model_id = Column(String)
    # The ISO 8601 timestamp of when the test was executed.
    timestamp_utc = Column(DateTime)
    # The complete, unmodified response from the LLM.
    raw_response = Column(String, nullable=True)
    # Any error message captured during the run. Null if successful.
    error = Column(String, nullable=True)
    # The deterministic classification assigned by the Classifier (stored as JSON).
    classification = Column(JSON, nullable=True)
    # Quantitative scores assigned by the Scorer (stored as JSON).
    scores = Column(JSON, nullable=True)