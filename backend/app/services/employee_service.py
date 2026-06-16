from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.employee import Employee
from app.models.department import Department
from app.models.designation import Designation


class EmployeeService:
    """Manages employee records and operations"""

    @staticmethod
    def search_employees(query: str, db: Session) -> list:
        """Search employees by name, email, or code"""
        return db.query(Employee).filter(
            or_(
                Employee.first_name.ilike(f"%{query}%"),
                Employee.last_name.ilike(f"%{query}%"),
                Employee.email.ilike(f"%{query}%"),
                Employee.employee_code.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def get_employees_by_department(department_id: int, db: Session) -> list:
        """Get all employees in a department"""
        return db.query(Employee).filter(Employee.department_id == department_id).all()

    @staticmethod
    def get_employees_by_manager(manager_id: int, db: Session) -> list:
        """Get all employees reporting to a manager"""
        return db.query(Employee).filter(Employee.manager_id == manager_id).all()

    @staticmethod
    def get_active_employees(db: Session) -> list:
        """Get all active employees"""
        return db.query(Employee).filter(Employee.status == "Active").all()

    @staticmethod
    def get_inactive_employees(db: Session) -> list:
        """Get all inactive employees"""
        return db.query(Employee).filter(Employee.status == "Inactive").all()

    @staticmethod
    def get_employees_by_designation(designation_id: int, db: Session) -> list:
        """Get all employees with a specific designation"""
        return db.query(Employee).filter(Employee.designation_id == designation_id).all()

    @staticmethod
    def get_department_statistics(db: Session) -> list:
        """Get employee count per department"""
        departments = db.query(Department).all()
        stats = []
        for dept in departments:
            count = db.query(Employee).filter(Employee.department_id == dept.id).count()
            stats.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "employee_count": count
            })
        return stats

    @staticmethod
    def get_designation_statistics(db: Session) -> list:
        """Get employee count per designation"""
        designations = db.query(Designation).all()
        stats = []
        for desig in designations:
            count = db.query(Employee).filter(Employee.designation_id == desig.id).count()
            stats.append({
                "designation_id": desig.id,
                "designation_title": desig.title,
                "employee_count": count
            })
        return stats

    @staticmethod
    def export_employee_data(db: Session) -> list:
        """Export all employee data for reports"""
        employees = db.query(Employee).all()
        data = []
        for emp in employees:
            data.append({
                "employee_code": emp.employee_code,
                "name": f"{emp.first_name} {emp.last_name}",
                "email": emp.email,
                "mobile": emp.mobile_number,
                "department": emp.department.name if emp.department else "N/A",
                "designation": emp.designation.title if emp.designation else "N/A",
                "salary": emp.salary,
                "date_of_joining": emp.date_of_joining.strftime("%Y-%m-%d") if emp.date_of_joining else "N/A",
                "status": emp.status
            })
        return data
