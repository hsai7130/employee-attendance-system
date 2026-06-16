from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.leave import LeaveRequestCreate, LeaveRequestResponse, LeaveRequestUpdate
from app.services.leave_service import LeaveRequestService, LeaveBalanceService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/apply", response_model=LeaveRequestResponse, dependencies=[Depends(require_role(["Employee"]))])
def apply_leave(leave_in: LeaveRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Employee applies for leave"""
    try:
        # Check if employee can apply leave
        if not LeaveRequestService.can_apply_leave(leave_in.employee_id, leave_in.start_date, leave_in.end_date, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Overlapping approved leave exists")
        
        leave_request = LeaveRequestService.apply_leave(
            leave_in.employee_id, leave_in.leave_type_id, leave_in.start_date, 
            leave_in.end_date, leave_in.reason, db
        )
        AuditService.log_action(current_user.id, "APPLY_LEAVE", "leave_request", str(leave_request.id), db=db)
        return leave_request
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{leave_id}/approve", response_model=LeaveRequestResponse, dependencies=[Depends(require_role(["Manager", "HR Admin"]))])
def approve_leave(leave_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Manager/HR approves leave request"""
    try:
        leave_request = LeaveRequestService.approve_leave(leave_id, current_user.id, db)
        AuditService.log_action(current_user.id, "APPROVE_LEAVE", "leave_request", str(leave_id), db=db)
        return leave_request
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{leave_id}/reject", response_model=LeaveRequestResponse, dependencies=[Depends(require_role(["Manager", "HR Admin"]))])
def reject_leave(leave_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Manager/HR rejects leave request"""
    try:
        leave_request = LeaveRequestService.reject_leave(leave_id, current_user.id, db)
        AuditService.log_action(current_user.id, "REJECT_LEAVE", "leave_request", str(leave_id), db=db)
        return leave_request
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/pending", response_model=list[LeaveRequestResponse], dependencies=[Depends(require_role(["Manager", "HR Admin"]))])
def get_pending_leaves(employee_id: int = None, db: Session = Depends(get_db)):
    """Get pending leave requests"""
    return LeaveRequestService.get_pending_leaves(employee_id, db)


@router.get("/balance/{employee_id}/{year}", dependencies=[Depends(require_role(["Employee", "Manager", "HR Admin"]))])
def get_leave_balance(employee_id: int, year: int, db: Session = Depends(get_db)):
    """Get leave balance for employee"""
    return LeaveBalanceService.get_all_leave_balances(employee_id, year, db)


@router.get("/history/{employee_id}/{year}", response_model=list[LeaveRequestResponse], dependencies=[Depends(require_role(["Employee", "Manager", "HR Admin"]))])
def get_leave_history(employee_id: int, year: int, db: Session = Depends(get_db)):
    """Get leave history for employee"""
    return LeaveRequestService.get_employee_leave_history(employee_id, year, db)
