# Backend README

## Requirements

- Python 3.12
- Poetry
- PostgreSQL

## Run Locally

1. `cd backend`
2. `poetry install`
3. `poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Environment

Set environment variables in `.env`:

- `SQLALCHEMY_DATABASE_URI`
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## API Endpoints

- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/employees`
- `GET /api/employees`
- `POST /api/attendance`
- `POST /api/leave`
- `POST /api/payroll/process`
