from datetime import date
from pydantic import BaseModel


class LeaveRequestBase(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    days: int
    reason: str | None = None


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(LeaveRequestBase):
    status: str | None = None


class LeaveRequestResponse(LeaveRequestBase):
    id: int
    status: str

    class Config:
        orm_mode = True
