from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.models.attendance import Attendance, AttendanceStatus
from app.models.leave_request import LeaveRequest, LeaveStatus
from app.models.payroll import Payroll
from app.models.employee import Employee


class ReportService:
    """Generates various reports"""

    @staticmethod
    def attendance_report(start_date: date, end_date: date, db: Session) -> dict:
        """Generate attendance report for a date range"""
        records = db.query(Attendance).filter(
            and_(Attendance.date >= start_date, Attendance.date <= end_date)
        ).all()
        
        status_summary = {}
        for status in AttendanceStatus:
            count = sum(1 for r in records if r.status == status.value)
            status_summary[status.value] = count
        
        employee_attendance = {}
        for record in records:
            emp_id = record.employee_id
            if emp_id not in employee_attendance:
                employee_attendance[emp_id] = {"present": 0, "absent": 0, "half_day": 0}
            
            if record.status == AttendanceStatus.PRESENT.value:
                employee_attendance[emp_id]["present"] += 1
            elif record.status == AttendanceStatus.ABSENT.value:
                employee_attendance[emp_id]["absent"] += 1
            elif record.status == AttendanceStatus.HALF_DAY.value:
                employee_attendance[emp_id]["half_day"] += 1
        
        return {
            "report_type": "Attendance Report",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_records": len(records),
            "status_summary": status_summary,
            "employee_attendance": employee_attendance
        }

    @staticmethod
    def leave_report(year: int, db: Session) -> dict:
        """Generate leave report for a year"""
        leaves = db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.start_date >= date(year, 1, 1),
                LeaveRequest.start_date <= date(year, 12, 31)
            )
        ).all()
        
        leave_summary = {
            "total_applied": len(leaves),
            "approved": sum(1 for l in leaves if l.status == LeaveStatus.APPROVED.value),
            "rejected": sum(1 for l in leaves if l.status == LeaveStatus.REJECTED.value),
            "pending": sum(1 for l in leaves if l.status == LeaveStatus.PENDING.value),
            "total_days": sum(l.days for l in leaves if l.status == LeaveStatus.APPROVED.value)
        }
        
        by_leave_type = {}
        for leave in leaves:
            leave_type = leave.leave_type.name
            if leave_type not in by_leave_type:
                by_leave_type[leave_type] = 0
            by_leave_type[leave_type] += leave.days
        
        return {
            "report_type": "Leave Report",
            "year": year,
            "summary": leave_summary,
            "by_leave_type": by_leave_type,
            "total_records": len(leaves)
        }

    @staticmethod
    def payroll_report(year: int, month: int, db: Session) -> dict:
        """Generate payroll report for a month"""
        month_name = date(year, month, 1).strftime("%B")
        payrolls = db.query(Payroll).filter(
            and_(Payroll.period_month == month_name, Payroll.period_year == year)
        ).all()
        
        total_gross = sum(p.gross_salary for p in payrolls)
        total_allowances = sum(p.allowances for p in payrolls)
        total_deductions = sum(p.deductions + p.lop_deduction for p in payrolls)
        total_net = sum(p.net_salary for p in payrolls)
        
        return {
            "report_type": "Payroll Report",
            "period": f"{month_name} {year}",
            "total_employees": len(payrolls),
            "total_gross_salary": total_gross,
            "total_allowances": total_allowances,
            "total_deductions": total_deductions,
            "total_net_salary": total_net,
            "average_salary": total_net / len(payrolls) if payrolls else 0
        }

    @staticmethod
    def department_attendance_report(department_id: int, month: int, year: int, db: Session) -> dict:
        """Generate attendance report for a department"""
        employees = db.query(Employee).filter(Employee.department_id == department_id).all()
        
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        emp_attendance = []
        for emp in employees:
            records = db.query(Attendance).filter(
                and_(
                    Attendance.employee_id == emp.id,
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).all()
            
            present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT.value)
            absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT.value)
            half_day = sum(1 for r in records if r.status == AttendanceStatus.HALF_DAY.value)
            
            emp_attendance.append({
                "employee_code": emp.employee_code,
                "name": f"{emp.first_name} {emp.last_name}",
                "present": present,
                "absent": absent,
                "half_day": half_day,
                "working_days": present + half_day
            })
        
        return {
            "report_type": "Department Attendance Report",
            "department_id": department_id,
            "period": f"{date(year, month, 1).strftime('%B %Y')}",
            "total_employees": len(emp_attendance),
            "employees": emp_attendance
        }

    @staticmethod
    def employee_summary_report(employee_id: int, year: int, db: Session) -> dict:
        """Generate comprehensive summary for an employee"""
        employee = db.query(Employee).get(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        
        # Attendance
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        attendance_records = db.query(Attendance).filter(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        ).all()
        
        # Leaves
        leaves = db.query(LeaveRequest).filter(
            and_(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.start_date >= start_date,
                LeaveRequest.start_date <= end_date,
                LeaveRequest.status == LeaveStatus.APPROVED.value
            )
        ).all()
        
        # Payroll
        payrolls = db.query(Payroll).filter(
            and_(Payroll.employee_id == employee_id, Payroll.period_year == year)
        ).all()
        
        return {
            "report_type": "Employee Summary Report",
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "year": year,
            "attendance": {
                "total_working_days": len(attendance_records),
                "present": sum(1 for r in attendance_records if r.status == AttendanceStatus.PRESENT.value),
                "absent": sum(1 for r in attendance_records if r.status == AttendanceStatus.ABSENT.value),
                "half_day": sum(1 for r in attendance_records if r.status == AttendanceStatus.HALF_DAY.value)
            },
            "leave": {
                "total_approved": len(leaves),
                "total_days_taken": sum(l.days for l in leaves)
            },
            "payroll": {
                "total_payrolls": len(payrolls),
                "total_net_salary": sum(p.net_salary for p in payrolls)
            }
        }
