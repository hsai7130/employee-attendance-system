from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/attendance/{start_date}/{end_date}", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def attendance_report(start_date: str, end_date: str, db: Session = Depends(get_db)):
    """Generate attendance report"""
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        return ReportService.attendance_report(start, end, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/leave/{year}", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def leave_report(year: int, db: Session = Depends(get_db)):
    """Generate leave report for a year"""
    return ReportService.leave_report(year, db)


@router.get("/payroll/{year}/{month}", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def payroll_report(year: int, month: int, db: Session = Depends(get_db)):
    """Generate payroll report"""
    return ReportService.payroll_report(year, month, db)


@router.get("/department-attendance/{department_id}/{year}/{month}", dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def department_attendance_report(department_id: int, year: int, month: int, db: Session = Depends(get_db)):
    """Generate department attendance report"""
    return ReportService.department_attendance_report(department_id, month, year, db)


@router.get("/employee-summary/{employee_id}/{year}", dependencies=[Depends(require_role(["Employee", "Manager", "HR Admin"]))])
def employee_summary_report(employee_id: int, year: int, db: Session = Depends(get_db)):
    """Generate employee summary report"""
    try:
        return ReportService.employee_summary_report(employee_id, year, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
