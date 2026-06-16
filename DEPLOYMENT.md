# Deployment Guide

## Docker Deployment

1. Build and run containers:
   ```bash
   docker-compose up --build
   ```
2. Backend: `http://localhost:8000`
3. Frontend: `http://localhost:3000`

## AWS Deployment

- Build backend and frontend images.
- Push to Amazon ECR.
- Deploy backend and frontend containers using ECS Fargate.
- Use AWS RDS for PostgreSQL.
- Front door via Application Load Balancer.
- Store secrets in AWS Secrets Manager or Parameter Store.

## Azure Deployment

- Build images and push to Azure Container Registry.
- Use Azure App Service for Containers or Azure Container Apps.
- Use Azure Database for PostgreSQL.
- Configure environment variables in Azure App Service.
- Use Application Gateway or Azure Front Door for HTTPS.

## Nginx Reverse Proxy

Example configuration:

```nginx
server {
    listen 80;
    server_name example.com;

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
    }
}
```

## Environment Variables

- `SQLALCHEMY_DATABASE_URI`
- `JWT_SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `BACKEND_CORS_ORIGINS`

## Notes

- Use HTTPS in production.
- Rotate JWT secret periodically.
- Add monitoring and logging for ECS/Azure containers.
