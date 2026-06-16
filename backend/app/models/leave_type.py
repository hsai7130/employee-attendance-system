from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class LeaveType(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(30), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    leave_requests = relationship("LeaveRequest", back_populates="leave_type")
