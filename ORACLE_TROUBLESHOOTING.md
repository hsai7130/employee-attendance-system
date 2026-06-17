# Oracle Cloud - Troubleshooting Guide

## Common Issues & Solutions

### SSH Connection Issues

#### ❌ "Permission denied (publickey)"
```
Error: Permission denied (publickey).
```

**Solution**:
1. Check key file permissions:
   ```bash
   chmod 600 attendance-backend.key
   ```

2. Verify you're using the correct key:
   ```bash
   # Right way
   ssh -i attendance-backend.key ubuntu@YOUR_IP
   
   # Wrong way
   ssh ubuntu@YOUR_IP  # This won't work
   ```

3. Check SSH key format (.pem file):
   ```bash
   # Should start with:
   # -----BEGIN RSA PRIVATE KEY-----
   cat attendance-backend.key | head -1
   ```

#### ❌ "Connection timeout"
```
Error: ssh: connect to host X.X.X.X port 22: Connection timed out
```

**Solution**:
1. Wait 5 minutes after instance shows "RUNNING"
2. Check Oracle Cloud Security List allows SSH (port 22):
   - Oracle Console → Networking → Virtual Cloud Networks
   - Find your VCN → Security Lists
   - Check Ingress Rules include port 22

#### ❌ "Could not resolve hostname"
```
Error: ssh: Could not resolve hostname ...
```

**Solution**:
- Copy the exact PUBLIC_IP_ADDRESS from Oracle Console
- No typos!
- Example: `ssh -i key.pem ubuntu@132.145.226.34`

---

### Docker Issues

#### ❌ "docker: command not found"
```
Error: docker: command not found
```

**Solution**:
```bash
# Reinstall Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Add user to docker group (if not done)
sudo usermod -aG docker ubuntu
newgrp docker

# Verify
docker --version
```

#### ❌ "permission denied while trying to connect to Docker daemon"
```
Error: Got permission denied while trying to connect to the Docker daemon
```

**Solution**:
```bash
# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Activate group (don't need to logout)
newgrp docker

# Verify
docker ps
```

#### ❌ Container exits immediately
```
docker ps shows no running container
```

**Solution**:
```bash
# Check logs
docker logs attendance-backend

# If error shown, fix issue and restart
docker restart attendance-backend

# Monitor logs live
docker logs -f attendance-backend
```

#### ❌ "port 8000 is already in use"
```
Error: bind: address already in use
```

**Solution**:
```bash
# Stop existing container
docker stop attendance-backend

# Remove it
docker rm attendance-backend

# Run new one
docker run -d --name attendance-backend -p 8000:8000 --env-file .env attendance-backend
```

---

### Database Connection Issues

#### ❌ "could not connect to server: Connection refused"
```
Error: sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**:
1. Check database status in Oracle Console:
   - Should show "AVAILABLE" (green)
   - If still provisioning, wait 10 minutes

2. Verify DATABASE_URL is correct:
   ```bash
   # Check your .env file
   cat .env | grep DATABASE_URL
   
   # Should look like:
   # postgresql+psycopg://postgres:PASSWORD@attendance-db.subnets.oraclevcn.com:5432/postgres
   ```

3. Test database connection manually:
   ```bash
   # Install psql client
   sudo apt install postgresql-client -y
   
   # Test connection (replace PASSWORD and HOST)
   psql -h attendance-db.subnets.oraclevcn.com \
        -U postgres \
        -d postgres \
        -c "SELECT 1"
   
   # Should return: 1
   ```

#### ❌ "authentication failed for user postgres"
```
Error: FATAL: password authentication failed for user "postgres"
```

**Solution**:
- Check password in .env matches database password from Step 2
- Recheck Oracle Console for correct password
- If unsure, reset in Oracle Console and update .env

#### ❌ "name or service not known"
```
Error: could not translate host name "attendance-db.subnets.oraclevcn.com"
```

**Solution**:
1. Check hostname is exactly correct (copy from Oracle Console)
2. Test DNS resolution:
   ```bash
   nslookup attendance-db.subnets.oraclevcn.com
   ```

3. Check instance is on same VCN as database:
   - Compute Instance → VCN: should match Database VCN

---

### API Issues

#### ❌ "Cannot GET /api/health"
```
Browser shows: 404 Cannot GET /api/health
```

**Solution**:
1. Check backend is running:
   ```bash
   docker ps | grep attendance-backend
   ```

2. Check logs for startup errors:
   ```bash
   docker logs attendance-backend
   ```

3. Wait 10 seconds after docker run (startup time)

4. Try again with full URL:
   ```bash
   curl http://YOUR_IP:8000/api/health
   ```

#### ❌ CORS errors in browser
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**:
1. Check BACKEND_CORS_ORIGINS in .env:
   ```bash
   cat .env | grep CORS
   # Should be: https://your-vercel-project.vercel.app
   ```

2. Update .env if wrong:
   ```bash
   nano .env
   # Update BACKEND_CORS_ORIGINS to exact Vercel URL
   # Save with Ctrl+X, Y, Enter
   ```

3. Restart container:
   ```bash
   docker restart attendance-backend
   ```

#### ❌ "500 Internal Server Error"
```
API returns: 500 Internal Server Error
```

**Solution**:
1. Check Docker logs:
   ```bash
   docker logs -f attendance-backend
   # Watch for error messages
   ```

2. Common causes:
   - Database connection failed → fix DATABASE_URL
   - JWT_SECRET_KEY not set → add to .env
   - Missing dependencies → rebuild Docker image

3. Rebuild if needed:
   ```bash
   docker stop attendance-backend
   docker rm attendance-backend
   docker build -t attendance-backend .
   docker run -d --name attendance-backend -p 8000:8000 --env-file .env attendance-backend
   ```

---

### Vercel Frontend Issues

#### ❌ "Cannot reach backend"
```
Frontend shows: Failed to fetch from API
```

**Solution**:
1. Check NEXT_PUBLIC_API_URL in Vercel:
   - Vercel → Project → Settings → Environment Variables
   - Should be: `http://YOUR_PUBLIC_IP:8000`

2. Redeploy Vercel:
   - Go to Deployments tab
   - Click "Redeploy" on latest

3. Clear browser cache:
   - F12 → Application → Clear storage
   - Or: Ctrl+Shift+Delete

#### ❌ "Login fails silently"
```
Click login, nothing happens
```

**Solution**:
1. Open DevTools (F12)
2. Go to Console tab
3. Look for errors (usually CORS or network)
4. Check Network tab during login attempt
5. Look at response to /api/auth/login

---

### Memory/Performance Issues

#### ❌ Backend crashes randomly
```
Container exits without error message
```

**Solution**:
1. Check Oracle instance memory:
   ```bash
   free -h
   ```

2. Check Docker container resource usage:
   ```bash
   docker stats
   ```

3. If out of memory:
   - Upgrade instance (paid)
   - Or optimize code/queries

#### ❌ Slow response times
```
API takes 10+ seconds to respond
```

**Solution**:
1. Check CPU/Memory:
   ```bash
   top
   docker stats
   ```

2. Check database performance:
   ```bash
   # From inside container
   docker exec attendance-backend bash
   psql [connection string] -c "SELECT count(*) FROM employees;"
   ```

3. Restart container (might help):
   ```bash
   docker restart attendance-backend
   ```

---

### Git & Code Issues

#### ❌ "Permission denied" when pushing code
```
Error: Permission denied (publickey)
```

**Solution**:
```bash
# Generate new SSH key for GitHub
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Add to GitHub:
# GitHub → Settings → SSH and GPG keys
# → New SSH key
# Paste the content of id_rsa.pub
```

#### ❌ "Repository not found"
```
Error: Repository not found
```

**Solution**:
1. Verify repo URL:
   ```bash
   git clone https://github.com/YOUR_USERNAME/employee-attendance-system.git
   ```

2. Check username is correct
3. Check repo exists and you have access
4. Might need to use HTTPS instead of SSH:
   ```bash
   git clone https://github.com/YOUR_USERNAME/employee-attendance-system.git
   ```

---

## How to Get Help

### 1. Check Logs First
```bash
# Docker logs
docker logs attendance-backend

# System logs
journalctl -u attendance-backend.service -n 50

# Nginx logs (if using HTTPS)
sudo tail -f /var/log/nginx/error.log
```

### 2. Test Components Individually
```bash
# Test database
psql -h [host] -U [user] -d [db] -c "SELECT 1"

# Test API health
curl http://YOUR_IP:8000/api/health

# Test frontend connectivity
curl https://YOUR_VERCEL_URL
```

### 3. Check Resource Usage
```bash
# Disk space
df -h

# Memory
free -h

# CPU
top -b -n 1

# Docker stats
docker stats
```

---

## Rollback / Reset

### Stop Everything
```bash
docker stop attendance-backend
docker rm attendance-backend
```

### Start Fresh
```bash
cd employee-attendance-system/backend

# Update code from GitHub
git pull origin main

# Rebuild image
docker build -t attendance-backend .

# Run again
docker run -d --name attendance-backend -p 8000:8000 --env-file .env attendance-backend
```

### Check Status
```bash
docker ps
docker logs -f attendance-backend
curl http://YOUR_IP:8000/api/health
```

---

## Support Resources

- **Oracle Cloud Docs**: https://docs.oracle.com/en-us/iaas/
- **Docker Docs**: https://docs.docker.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Ubuntu Help**: https://help.ubuntu.com/

---

**Still stuck? Check the logs! 99% of issues show up there.**
