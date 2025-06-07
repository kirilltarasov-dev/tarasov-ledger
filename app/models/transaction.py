from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    raw_text = Column(Text, nullable=False)
    filename = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    vendor = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    amount_currency = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    category = Column(String, nullable=True)
