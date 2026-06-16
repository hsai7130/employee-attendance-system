from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role, get_current_user
from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services.employee_service import EmployeeService
from app.services.audit_service import AuditService

router = APIRouter()


@router.post("/", response_model=EmployeeResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new employee"""
    existing = db.query(Employee).filter(Employee.employee_code == employee_in.employee_code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee code already exists")
    employee = Employee(**employee_in.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    AuditService.log_action(current_user.id, "CREATE_EMPLOYEE", "employee", str(employee.id), db=db)
    return employee


@router.get("/search", response_model=list[EmployeeResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def search_employees(q: str, db: Session = Depends(get_db)):
    """Search employees by name, email, or code"""
    return EmployeeService.search_employees(q, db)


@router.get("/", response_model=list[EmployeeResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def get_employees(skip: int = 0, limit: int = 50, status: str = None, db: Session = Depends(get_db)):
    """Get all employees"""
    query = db.query(Employee)
    if status:
        query = query.filter(Employee.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{employee_id}", response_model=EmployeeResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager", "Employee"]))])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee details"""
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse, dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def update_employee(employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update employee details"""
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    for field, value in employee_in.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    AuditService.log_action(current_user.id, "UPDATE_EMPLOYEE", "employee", str(employee_id), db=db)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete employee (soft delete by marking inactive)"""
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    employee.status = "Inactive"
    db.add(employee)
    db.commit()
    AuditService.log_action(current_user.id, "DELETE_EMPLOYEE", "employee", str(employee_id), db=db)


@router.get("/department/{department_id}", response_model=list[EmployeeResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def get_employees_by_department(department_id: int, db: Session = Depends(get_db)):
    """Get employees in a department"""
    return EmployeeService.get_employees_by_department(department_id, db)


@router.get("/manager/{manager_id}", response_model=list[EmployeeResponse], dependencies=[Depends(require_role(["Super Admin", "HR Admin", "Manager"]))])
def get_employees_by_manager(manager_id: int, db: Session = Depends(get_db)):
    """Get employees reporting to a manager"""
    return EmployeeService.get_employees_by_manager(manager_id, db)


@router.get("/statistics/departments", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def get_department_statistics(db: Session = Depends(get_db)):
    """Get employee count per department"""
    return EmployeeService.get_department_statistics(db)


@router.get("/export/all", dependencies=[Depends(require_role(["Super Admin", "HR Admin"]))])
def export_employee_data(db: Session = Depends(get_db)):
    """Export all employee data"""
    return EmployeeService.export_employee_data(db)
