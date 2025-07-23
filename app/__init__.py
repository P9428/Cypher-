"""RoyaltyRails core package."""

from .database import SessionLocal, engine, Base


def init_db():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)
