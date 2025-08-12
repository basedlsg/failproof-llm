"""
Handles the database connection and session management.

This module is responsible for setting up the connection to the SQLite database.
It defines the database URL, creates the SQLAlchemy engine, and provides a
session factory (`SessionLocal`) for creating new database sessions.

The `check_same_thread` argument is specific to SQLite and is required to
allow the database connection to be shared across different threads, which
is necessary for web applications like FastAPI.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# The location of the SQLite database file.
DATABASE_URL = "sqlite:///./failproof_llm.db"

# The SQLAlchemy engine is the starting point for any SQLAlchemy application.
# It's the low-level object that manages connections to the database.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for creating new Session objects. A Session is
# the primary interface for all database operations in the ORM.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)