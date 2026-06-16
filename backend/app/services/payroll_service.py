from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.payroll import Payroll
from app.models.employee import Employee
from app.models.attendance import Attendance, AttendanceStatus
from app.models.leave_request import LeaveRequest, LeaveStatus


class PayrollService:
    """Manages payroll processing and salary calculations"""
    
    TAX_RATE = 0.10  # 10% tax rate
    WORKING_DAYS_PER_MONTH = 22  # Average working days

    @staticmethod
    def calculate_lop_deduction(employee_id: int, year: int, month: int, db: Session) -> float:
        """Calculate Loss of Pay (LOP) deduction based on absences"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        employee = db.query(Employee).get(employee_id)
        if not employee or not employee.salary:
            return 0.0
        
        # Count absent days
        absents = db.query(Attendance).filter(
            and_(
                Attendance.employee_id == employee_id,
                Attendance.date >= start_date,
                Attendance.date < end_date,
                Attendance.status == AttendanceStatus.ABSENT.value
            )
        ).count()
        
        daily_salary = employee.salary / PayrollService.WORKING_DAYS_PER_MONTH
        return absents * daily_salary

    @staticmethod
    def calculate_allowances(employee_id: int, db: Session) -> float:
        """Calculate allowances (DA, HRA, etc.)"""
        employee = db.query(Employee).get(employee_id)
        if not employee or not employee.salary:
            return 0.0
        
        # Example: 30% of salary as allowances (DA + HRA + other)
        return employee.salary * 0.30

    @staticmethod
    def calculate_tax_deduction(gross_salary: float) -> float:
        """Calculate income tax deduction"""
        # Simple tax calculation: 10% of gross salary
        return gross_salary * PayrollService.TAX_RATE

    @staticmethod
    def process_payroll(employee_id: int, year: int, month: int, db: Session) -> Payroll:
        """Process payroll for an employee"""
        employee = db.query(Employee).get(employee_id)
        if not employee or not employee.salary:
            raise ValueError("Employee not found or has no salary set")
        
        gross_salary = employee.salary
        allowances = PayrollService.calculate_allowances(employee_id, db)
        lop_deduction = PayrollService.calculate_lop_deduction(employee_id, year, month, db)
        tax_deduction = PayrollService.calculate_tax_deduction(gross_salary + allowances)
        
        total_deductions = lop_deduction + tax_deduction
        net_salary = (gross_salary + allowances) - total_deductions
        
        payroll = Payroll(
            employee_id=employee_id,
            period_month=date(year, month, 1).strftime("%B"),
            period_year=year,
            gross_salary=gross_salary,
            allowances=allowances,
            deductions=tax_deduction,
            lop_deduction=lop_deduction,
            net_salary=max(0, net_salary)
        )
        
        db.add(payroll)
        db.commit()
        db.refresh(payroll)
        return payroll

    @staticmethod
    def get_payroll_for_period(year: int, month: int, db: Session) -> list:
        """Get payroll records for a specific period"""
        month_name = date(year, month, 1).strftime("%B")
        return db.query(Payroll).filter(
            and_(Payroll.period_month == month_name, Payroll.period_year == year)
        ).all()

    @staticmethod
    def get_salary_register(year: int, month: int, db: Session) -> dict:
        """Generate salary register for a month"""
        payrolls = PayrollService.get_payroll_for_period(year, month, db)
        
        total_gross = sum(p.gross_salary for p in payrolls)
        total_allowances = sum(p.allowances for p in payrolls)
        total_deductions = sum(p.deductions + p.lop_deduction for p in payrolls)
        total_net = sum(p.net_salary for p in payrolls)
        
        return {
            "period": f"{date(year, month, 1).strftime('%B %Y')}",
            "total_employees": len(payrolls),
            "total_gross_salary": total_gross,
            "total_allowances": total_allowances,
            "total_deductions": total_deductions,
            "total_net_salary": total_net,
            "payrolls": payrolls
        }

    @staticmethod
    def get_employee_payslips(employee_id: int, year: int, db: Session) -> list:
        """Get all payslips for an employee in a year"""
        return db.query(Payroll).filter(
            and_(Payroll.employee_id == employee_id, Payroll.period_year == year)
        ).all()

    @staticmethod
    def generate_payslip_data(payroll_id: int, db: Session) -> dict:
        """Generate data for payslip PDF"""
        payroll = db.query(Payroll).get(payroll_id)
        if not payroll:
            raise ValueError("Payroll record not found")
        
        employee = db.query(Employee).get(payroll.employee_id)
        
        return {
            "payroll_id": payroll.id,
            "employee_code": employee.employee_code,
            "employee_name": f"{employee.first_name} {employee.last_name}",
            "department": employee.department.name if employee.department else "N/A",
            "designation": employee.designation.title if employee.designation else "N/A",
            "period": f"{payroll.period_month} {payroll.period_year}",
            "gross_salary": payroll.gross_salary,
            "allowances": payroll.allowances,
            "gross_pay": payroll.gross_salary + payroll.allowances,
            "tax_deduction": payroll.deductions,
            "lop_deduction": payroll.lop_deduction,
            "total_deductions": payroll.deductions + payroll.lop_deduction,
            "net_salary": payroll.net_salary,
            "issued_date": datetime.utcnow().strftime("%Y-%m-%d")
        }
