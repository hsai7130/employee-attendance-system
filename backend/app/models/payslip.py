from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    payroll_id = Column(Integer, ForeignKey("payroll.id"), nullable=False)
    pdf_path = Column(String(255), nullable=True)
    issued_at = Column(DateTime, default=datetime.utcnow)

    payroll = relationship("Payroll")
