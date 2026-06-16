from datetime import date, datetime
from sqlalchemy import Column, Date, Integer, String

from app.db.base import Base


class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
