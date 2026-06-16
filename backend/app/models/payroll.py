from datetime import date, datetime
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Payroll(Base):
    __tablename__ = "payroll"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    period_month = Column(String(20), nullable=False)
    period_year = Column(Integer, nullable=False)
    gross_salary = Column(Float, nullable=False)
    allowances = Column(Float, nullable=True, default=0.0)
    deductions = Column(Float, nullable=True, default=0.0)
    lop_deduction = Column(Float, nullable=True, default=0.0)
    net_salary = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = relationship("Employee")
