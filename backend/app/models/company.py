from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    domain = Column(String, unique=True, nullable=False)
    description = Column(Text, default="")
    industry = Column(String, default="")

    # Scores computed by Claude (0–1)
    cosell_score = Column(Float, default=0.0)
    buying_intent_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)

    # Embedding for semantic similarity search
    embedding = Column(Vector(1536), nullable=True)

    # Raw signals aggregated from open sources
    signals = Column(JSON, default=list)

    # Claude's reasoning / summary for the CEO
    claude_summary = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
