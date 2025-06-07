from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionExtracted(BaseModel):
    vendor: Optional[str] = None
    amount: Optional[float] = None
    amount_currency: Optional[str] = None
    date: Optional[datetime] = None
    category: Optional[str] = None
