from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.leave_request import LeaveRequest, LeaveStatus
from app.models.employee import Employee


class LeaveBalanceService:
    """Manages leave balance for employees"""
    
    LEAVE_BALANCE = {
        "Casual Leave": 12,
        "Sick Leave": 10,
        "Earned Leave": 20,
        "Optional Holiday": 2,
        "Loss Of Pay": 0,
    }

    @staticmethod
    def get_leave_balance(employee_id: int, leave_type: str, year: int, db: Session) -> dict:
        """Calculate remaining leave balance for an employee"""
        total_allowed = LeaveBalanceService.LEAVE_BALANCE.get(leave_type, 0)
        
        # Get all approved leaves for the year
        used_leaves = db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.leave_type.has(name=leave_type),
                LeaveRequest.status == LeaveStatus.APPROVED.value,
                LeaveRequest.start_date >= date(year, 1, 1),
                LeaveRequest.start_date <= date(year, 12, 31)
            )
        ).all()
        
        used_days = sum(r.days for r in used_leaves)
        remaining = total_allowed - used_days
        
        return {
            "leave_type": leave_type,
            "total_allowed": total_allowed,
            "used": used_days,
            "remaining": max(0, remaining)
        }

    @staticmethod
    def get_all_leave_balances(employee_id: int, year: int, db: Session) -> list:
        """Get leave balance for all leave types"""
        balances = []
        for leave_type in LeaveBalanceService.LEAVE_BALANCE.keys():
            balance = LeaveBalanceService.get_leave_balance(employee_id, leave_type, year, db)
            balances.append(balance)
        return balances


class LeaveRequestService:
    """Manages leave request workflow"""

    @staticmethod
    def apply_leave(employee_id: int, leave_type_id: int, start_date: date, 
                    end_date: date, reason: str, db: Session) -> LeaveRequest:
        """Apply for leave"""
        days = (end_date - start_date).days + 1
        
        leave_request = LeaveRequest(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            start_date=start_date,
            end_date=end_date,
            days=days,
            reason=reason,
            status=LeaveStatus.PENDING.value
        )
        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        return leave_request

    @staticmethod
    def approve_leave(leave_id: int, approver_id: int, db: Session) -> LeaveRequest:
        """Approve a leave request"""
        leave_request = db.query(LeaveRequest).get(leave_id)
        if not leave_request:
            raise ValueError("Leave request not found")
        
        leave_request.status = LeaveStatus.APPROVED.value
        leave_request.manager_id = approver_id
        leave_request.updated_at = datetime.utcnow()
        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        return leave_request

    @staticmethod
    def reject_leave(leave_id: int, rejector_id: int, db: Session) -> LeaveRequest:
        """Reject a leave request"""
        leave_request = db.query(LeaveRequest).get(leave_id)
        if not leave_request:
            raise ValueError("Leave request not found")
        
        leave_request.status = LeaveStatus.REJECTED.value
        leave_request.manager_id = rejector_id
        leave_request.updated_at = datetime.utcnow()
        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        return leave_request

    @staticmethod
    def get_pending_leaves(employee_id: int = None, db: Session = None) -> list:
        """Get pending leave requests"""
        query = db.query(LeaveRequest).filter(LeaveRequest.status == LeaveStatus.PENDING.value)
        if employee_id:
            query = query.filter(LeaveRequest.employee_id == employee_id)
        return query.all()

    @staticmethod
    def get_employee_leave_history(employee_id: int, year: int, db: Session) -> list:
        """Get leave history for an employee"""
        return db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.start_date >= date(year, 1, 1),
                LeaveRequest.start_date <= date(year, 12, 31)
            )
        ).all()

    @staticmethod
    def can_apply_leave(employee_id: int, start_date: date, end_date: date, db: Session) -> bool:
        """Check if employee can apply leave (no overlapping approved leaves)"""
        overlapping = db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status == LeaveStatus.APPROVED.value,
                LeaveRequest.start_date <= end_date,
                LeaveRequest.end_date >= start_date
            )
        ).first()
        
        return overlapping is None
