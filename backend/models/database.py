"""
SQLAlchemy database setup with environment-based configuration.
Supports both SQLite (local) and PostgreSQL (production).
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# Create engine based on environment
if settings.ENV == "production" and "postgresql" in settings.DATABASE_URL:
    # PostgreSQL configuration
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
else:
    # SQLite configuration (local development)
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        pool_pre_ping=True
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database session.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)
