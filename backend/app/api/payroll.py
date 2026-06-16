from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.payroll import PayrollCreate, PayrollResponse
from app.services.payroll_service import PayrollService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/process", response_model=PayrollResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def process_payroll(employee_id: int, year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Process payroll for an employee"""
    try:
        payroll = PayrollService.process_payroll(employee_id, year, month, db)
        AuditService.log_action(current_user.id, "PROCESS_PAYROLL", "payroll", str(payroll.id), db=db)
        return payroll
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/period/{year}/{month}", response_model=list[PayrollResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def get_payroll_for_period(year: int, month: int, db: Session = Depends(get_db)):
    """Get all payroll records for a period"""
    return PayrollService.get_payroll_for_period(year, month, db)


@router.get("/salary-register/{year}/{month}", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def get_salary_register(year: int, month: int, db: Session = Depends(get_db)):
    """Get salary register for a month"""
    return PayrollService.get_salary_register(year, month, db)


@router.get("/employee/{employee_id}/{year}", response_model=list[PayrollResponse], dependencies=[Depends(require_role(["Employee", "Manager", "HR Admin"]))])
def get_employee_payslips(employee_id: int, year: int, db: Session = Depends(get_db)):
    """Get employee payslips for a year"""
    return PayrollService.get_employee_payslips(employee_id, year, db)


@router.get("/payslip-data/{payroll_id}", dependencies=[Depends(require_role(["Employee", "Manager", "HR Admin"]))])
def get_payslip_data(payroll_id: int, db: Session = Depends(get_db)):
    """Get payslip data for PDF generation"""
    try:
        return PayrollService.generate_payslip_data(payroll_id, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
