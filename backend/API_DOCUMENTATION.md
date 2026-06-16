# API Documentation

## Authentication

### Login
```
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@company.com&password=password123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Register
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@company.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "password123",
  "role_id": 4
}
```

## Employees

### Create Employee
```
POST /api/employees
Authorization: Bearer {token}
Content-Type: application/json

{
  "employee_code": "EMP001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@company.com",
  "mobile_number": "9876543210",
  "department_id": 1,
  "designation_id": 1,
  "salary": 50000.00,
  "date_of_joining": "2024-01-15"
}
```

### Get All Employees
```
GET /api/employees?skip=0&limit=50
Authorization: Bearer {token}
```

### Search Employees
```
GET /api/employees/search?q=john
Authorization: Bearer {token}
```

### Get Employee by ID
```
GET /api/employees/{employee_id}
Authorization: Bearer {token}
```

### Update Employee
```
PUT /api/employees/{employee_id}
Authorization: Bearer {token}
Content-Type: application/json
```

### Delete Employee
```
DELETE /api/employees/{employee_id}
Authorization: Bearer {token}
```

## Attendance

### Check-In
```
POST /api/attendance/check-in?employee_id=1
Authorization: Bearer {token}
```

### Check-Out
```
POST /api/attendance/check-out?employee_id=1
Authorization: Bearer {token}
```

### Mark Manual Attendance
```
POST /api/attendance
Authorization: Bearer {token}
Content-Type: application/json

{
  "employee_id": 1,
  "date": "2024-06-16",
  "status": "Present",
  "remarks": "Regular working day"
}
```

### Get Monthly Attendance Summary
```
GET /api/attendance/monthly/2024/6?employee_id=1
Authorization: Bearer {token}
```

### Get Daily Attendance Summary
```
GET /api/attendance/daily/2024-06-16
Authorization: Bearer {token}
```

## Leave

### Apply Leave
```
POST /api/leave/apply
Authorization: Bearer {token}
Content-Type: application/json

{
  "employee_id": 1,
  "leave_type_id": 1,
  "start_date": "2024-06-20",
  "end_date": "2024-06-22",
  "days": 3,
  "reason": "Personal work"
}
```

### Get Leave Balance
```
GET /api/leave/balance/{employee_id}/2024
Authorization: Bearer {token}
```

### Approve Leave
```
PUT /api/leave/{leave_id}/approve
Authorization: Bearer {token}
```

### Reject Leave
```
PUT /api/leave/{leave_id}/reject
Authorization: Bearer {token}
```

### Get Pending Leaves
```
GET /api/leave/pending
Authorization: Bearer {token}
```

### Get Leave History
```
GET /api/leave/history/{employee_id}/2024
Authorization: Bearer {token}
```

## Payroll

### Process Payroll
```
POST /api/payroll/process?employee_id=1&year=2024&month=6
Authorization: Bearer {token}
```

### Get Payroll for Period
```
GET /api/payroll/period/2024/6
Authorization: Bearer {token}
```

### Get Salary Register
```
GET /api/payroll/salary-register/2024/6
Authorization: Bearer {token}
```

### Get Employee Payslips
```
GET /api/payroll/employee/{employee_id}/2024
Authorization: Bearer {token}
```

### Get Payslip Data
```
GET /api/payroll/payslip-data/{payroll_id}
Authorization: Bearer {token}
```

## Reports

### Attendance Report
```
GET /api/reports/attendance/2024-06-01/2024-06-30
Authorization: Bearer {token}
```

### Leave Report
```
GET /api/reports/leave/2024
Authorization: Bearer {token}
```

### Payroll Report
```
GET /api/reports/payroll/2024/6
Authorization: Bearer {token}
```

### Department Attendance Report
```
GET /api/reports/department-attendance/{department_id}/2024/6
Authorization: Bearer {token}
```

### Employee Summary Report
```
GET /api/reports/employee-summary/{employee_id}/2024
Authorization: Bearer {token}
```

## Role-Based Access Control

### Available Roles
1. **Super Admin** - Full system access
2. **HR Admin** - HR operations (employee, payroll, leave approval)
3. **Manager** - Team management (attendance, leave approval for team)
4. **Employee** - Personal operations (attendance, leave application)

### Endpoint Permissions

| Endpoint | Super Admin | HR Admin | Manager | Employee |
|----------|-------------|----------|---------|----------|
| POST /api/employees | ✅ | ✅ | ❌ | ❌ |
| GET /api/employees | ✅ | ✅ | ✅ | ❌ |
| POST /api/attendance/check-in | ✅ | ✅ | ✅ | ✅ |
| POST /api/leave/apply | ✅ | ✅ | ✅ | ✅ |
| PUT /api/leave/{id}/approve | ✅ | ✅ | ✅ | ❌ |
| POST /api/payroll/process | ✅ | ✅ | ❌ | ❌ |

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing the issue"
}
```

Common HTTP Status Codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Successful delete
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
