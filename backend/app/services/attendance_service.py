from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.attendance import Attendance, AttendanceStatus
from app.models.employee import Employee
from app.models.holiday import Holiday


class AttendanceService:
    @staticmethod
    def mark_check_in(employee_id: int, db: Session) -> Attendance:
        """Mark check-in for an employee"""
        today = date.today()
        attendance = db.query(Attendance).filter(
            and_(Attendance.employee_id == employee_id, Attendance.date == today)
        ).first()
        
        if not attendance:
            attendance = Attendance(
                employee_id=employee_id,
                date=today,
                check_in=datetime.now(),
                status=AttendanceStatus.PRESENT.value
            )
        else:
            attendance.check_in = datetime.now()
        
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance

    @staticmethod
    def mark_check_out(employee_id: int, db: Session) -> Attendance:
        """Mark check-out for an employee"""
        today = date.today()
        attendance = db.query(Attendance).filter(
            and_(Attendance.employee_id == employee_id, Attendance.date == today)
        ).first()
        
        if not attendance:
            raise ValueError("No check-in record found for today")
        
        attendance.check_out = datetime.now()
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance

    @staticmethod
    def get_monthly_attendance(employee_id: int, year: int, month: int, db: Session) -> dict:
        """Get attendance summary for a month"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        records = db.query(Attendance).filter(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).all()
        
        status_count = {}
        for record in records:
            status = record.status
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            "employee_id": employee_id,
            "year": year,
            "month": month,
            "total_days": len(records),
            "status_breakdown": status_count,
            "working_days": status_count.get(AttendanceStatus.PRESENT.value, 0)
        }

    @staticmethod
    def get_daily_summary(date_obj: date, db: Session) -> dict:
        """Get attendance summary for a specific day"""
        records = db.query(Attendance).filter(Attendance.date == date_obj).all()
        
        total = len(records)
        present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT.value)
        absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT.value)
        half_day = sum(1 for r in records if r.status == AttendanceStatus.HALF_DAY.value)
        wfh = sum(1 for r in records if r.status == AttendanceStatus.WORK_FROM_HOME.value)
        
        return {
            "date": date_obj,
            "total_employees": total,
            "present": present,
            "absent": absent,
            "half_day": half_day,
            "work_from_home": wfh
        }

    @staticmethod
    def get_late_arrivals(date_obj: date, threshold_hours: int = 1, db: Session = None) -> list:
        """Get list of employees who arrived late"""
        records = db.query(Attendance).filter(
            and_(Attendance.date == date_obj, Attendance.check_in.isnot(None))
        ).all()
        
        late_arrivals = []
        for record in records:
            if record.check_in.hour > threshold_hours:
                late_arrivals.append({
                    "employee_id": record.employee_id,
                    "check_in": record.check_in,
                    "delay_hours": record.check_in.hour - threshold_hours
                })
        
        return late_arrivals

    @staticmethod
    def get_missing_checkouts(date_obj: date, db: Session) -> list:
        """Get employees who didn't check out"""
        records = db.query(Attendance).filter(
            and_(
                Attendance.date == date_obj,
                Attendance.check_in.isnot(None),
                Attendance.check_out.isnull()
            )
        ).all()
        
        return [{"employee_id": r.employee_id, "check_in": r.check_in} for r in records]
