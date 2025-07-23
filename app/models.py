"""SQLAlchemy models."""
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class RightsHolder(Base):
    __tablename__ = 'rights_holders'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    wallet = Column(String, nullable=False)
    kyc_status = Column(String, default='pending')

    superfluid_stream_is_active = Column(Boolean, default=False)
    superfluid_flow_rate = Column(Integer, default=0)
    last_updated_tx_hash = Column(String, nullable=True)

    tokens = relationship('Token', back_populates='holder')

class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    track_id = Column(String, nullable=False)
    share = Column(Float, nullable=False)
    holder_id = Column(Integer, ForeignKey('rights_holders.id'))

    holder = relationship('RightsHolder', back_populates='tokens')

class StreamingData(Base):
    __tablename__ = 'streaming'
    id = Column(Integer, primary_key=True)
    track_id = Column(String, nullable=False)
    revenue = Column(Float, nullable=False)
    processed = Column(Boolean, default=False)
