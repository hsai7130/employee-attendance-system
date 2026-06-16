from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    gender: str | None = None
    date_of_birth: date | None = None
    mobile_number: str | None = None
    email: EmailStr
    department_id: int | None = None
    designation_id: int | None = None
    manager_id: int | None = None
    date_of_joining: date | None = None
    salary: float | None = None
    bank_name: str | None = None
    bank_account_number: str | None = None
    bank_ifsc: str | None = None
    pan_number: str | None = None
    aadhaar_number: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    status: str | None = "Active"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
