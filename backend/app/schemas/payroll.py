from pydantic import BaseModel


class PayrollBase(BaseModel):
    employee_id: int
    period_month: str
    period_year: int
    gross_salary: float
    allowances: float | None = 0.0
    deductions: float | None = 0.0
    lop_deduction: float | None = 0.0


class PayrollCreate(PayrollBase):
    pass


class PayrollResponse(PayrollBase):
    id: int
    net_salary: float

    class Config:
        orm_mode = True
