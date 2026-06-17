# Dockerfile for Railway Deployment

This Dockerfile is already in place and configured for Railway.

## What Railway Does Automatically:

1. **Detects the Dockerfile** in your backend folder
2. **Builds the image** with your Python dependencies
3. **Runs the container** with FastAPI
4. **Injects environment variables** we configured
5. **Manages HTTPS** and SSL certificates
6. **Scales automatically** based on demand

## Dockerfile Details:

```dockerfile
# Your backend/Dockerfile contains:
- Python 3.12 base image
- Poetry dependency management
- FastAPI application server (Uvicorn)
- Exposed port 8000
```

## Railway Port Detection:

Railway automatically:
- ✅ Detects FastAPI is listening on port 8000
- ✅ Assigns a public HTTPS URL
- ✅ Routes traffic to your app

No additional configuration needed!

## If You Need to Modify Dockerfile:

Only edit if you need to:
- Add system dependencies (apt-get packages)
- Change Python version
- Add build scripts

Changes are picked up automatically:
1. Push to GitHub
2. Railway rebuilds
3. New deployment created

## Database Initialization:

The FastAPI app includes database setup:
- SQLAlchemy models in `app/models/`
- Session management in `app/db/`
- Database will auto-create tables on first run
