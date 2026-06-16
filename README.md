# Employee Attendance, Leave, and Payroll Management System

A cloud-native enterprise web application built with Next.js, TypeScript, Tailwind CSS, Material UI, FastAPI, SQLAlchemy, and PostgreSQL.

## Project Structure

- `backend/` - FastAPI backend, SQLAlchemy models, authentication, API routes
- `frontend/` - Next.js frontend with responsive UI
- `docker-compose.yml` - Local development container orchestration

## Backend Setup

1. Install Poetry
2. `cd backend`
3. `poetry install`
4. `poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Frontend Setup

1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Docker

`docker-compose up --build`

## Features

- JWT authentication
- Role-based access control
- Employee master management
- Attendance logging
- Leave request workflow
- Payroll processing
- Responsive dashboard and reports

## Deployment

- Build frontend and backend containers
- Use Nginx as reverse proxy
- Deploy to AWS ECS or Azure App Service

## Notes

This starter project includes core schema definitions and base API endpoints. It is designed for extension into a production-ready system.
