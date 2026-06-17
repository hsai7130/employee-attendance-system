from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api import auth, employees, attendance, leave, payroll, reports
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Employee Attendance and Payroll API",
    version="1.0.0",
    description="Backend service for employee attendance, leave, and payroll management.",
)

origins = settings.CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(leave.router, prefix="/api/leave", tags=["Leave"])
app.include_router(payroll.router, prefix="/api/payroll", tags=["Payroll"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
