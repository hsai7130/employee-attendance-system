from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role, get_current_user
from app.models.attendance import Attendance
from app.models.user import User
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate
from app.services.attendance_service import AttendanceService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/check-in", response_model=AttendanceResponse, dependencies=[Depends(require_role(["Employee"]))])
def check_in(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Employee marks check-in"""
    try:
        attendance = AttendanceService.mark_check_in(employee_id, db)
        AuditService.log_action(current_user.id, "CHECK_IN", "attendance", str(attendance.id), db=db)
        return attendance
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/check-out", response_model=AttendanceResponse, dependencies=[Depends(require_role(["Employee"]))])
def check_out(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Employee marks check-out"""
    try:
        attendance = AttendanceService.mark_check_out(employee_id, db)
        AuditService.log_action(current_user.id, "CHECK_OUT", "attendance", str(attendance.id), db=db)
        return attendance
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=AttendanceResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def mark_attendance(attendance_in: AttendanceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Manual attendance entry"""
    attendance = Attendance(**attendance_in.model_dump())
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    AuditService.log_action(current_user.id, "MARK_ATTENDANCE", "attendance", str(attendance.id), db=db)
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def update_attendance(attendance_id: int, attendance_in: AttendanceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update attendance record"""
    attendance = db.get(Attendance, attendance_id)
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
    for field, value in attendance_in.model_dump(exclude_unset=True).items():
        setattr(attendance, field, value)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    AuditService.log_action(current_user.id, "UPDATE_ATTENDANCE", "attendance", str(attendance.id), db=db)
    return attendance


@router.get("/monthly/{year}/{month}", dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager", "Employee"]))])
def get_monthly_summary(employee_id: int, year: int, month: int, db: Session = Depends(get_db)):
    """Get monthly attendance summary"""
    try:
        return AttendanceService.get_monthly_attendance(employee_id, year, month, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/daily/{date_str}", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def get_daily_summary(date_str: str, db: Session = Depends(get_db)):
    """Get daily attendance summary"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return AttendanceService.get_daily_summary(date_obj, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[AttendanceResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def get_attendance_records(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Get attendance records"""
    return db.query(Attendance).offset(skip).limit(limit).all()
