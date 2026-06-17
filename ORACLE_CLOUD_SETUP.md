# Oracle Cloud Deployment - Complete Setup Guide

## Why Oracle Cloud?

✅ **Forever Free** (not just trial period)
✅ **Includes PostgreSQL database** (20GB)
✅ **2 ARM Compute instances**
✅ **Faster than other free options**
✅ **No credit card tricks**

---

## Phase 1: Create Oracle Cloud Account

### Step 1: Sign Up
1. Go to [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
2. Click "Start for free"
3. Enter email and password
4. Verify email
5. Choose region closest to you
6. **Skip adding payment method** (it's optional for free tier)

✅ Account created!

---

## Phase 2: Create PostgreSQL Database

### Step 2: Set Up Database
1. In Oracle Cloud Console, click **☰ (menu) → Databases → PostgreSQL**
2. Click **"Create DB System"**
3. **Configure**:
   - **Name**: `attendance-db`
   - **Username**: `postgres` (default)
   - **Password**: Create a strong password (save it!)
   - **Shape**: Keep default ARM (free)
   - **Storage**: 20GB (free limit)
   - **Backup**: Enable (automatic)
4. Click **"Create"** (takes 5-10 minutes)

✅ Database is provisioning...

### Step 3: Get Database Connection
1. Wait for DB to show "AVAILABLE" (green status)
2. Click the DB name
3. Copy these details:
   - **Hostname**: `attendance-db.subnets.oraclevcn.com`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **Username**: `postgres`
   - **Password**: (what you set above)

4. Build connection string:
```
postgresql+psycopg://postgres:YOUR_PASSWORD@attendance-db.subnets.oraclevcn.com:5432/postgres
```

**Save this!** You'll need it for backend.

---

## Phase 3: Create Compute Instance

### Step 4: Set Up VM for Backend
1. In Oracle Cloud Console, click **☰ → Compute → Instances**
2. Click **"Create Instance"**
3. **Configure**:
   - **Name**: `attendance-backend`
   - **Image**: Ubuntu 22.04 (free option)
   - **Shape**: Ampere (ARM) - Free tier eligible
   - **Network**: Create new or use default VCN
   - **SSH Key**: Download and save! (very important)
   - **Public IP**: Enabled ✅

4. Click **"Create"** (takes 2-3 minutes)

✅ Instance is launching...

### Step 5: Connect to Instance
1. Wait for instance to show "RUNNING" (green)
2. Click instance name to see details
3. Copy **Public IP Address**
4. Open terminal/PowerShell:

```powershell
# Navigate to where you saved SSH key
cd Downloads

# Connect to instance
ssh -i attendance-backend.key ubuntu@YOUR_PUBLIC_IP

# Accept connection prompt (type 'yes')
```

✅ You're now connected to your Oracle VM!

---

## Phase 4: Deploy Backend on Compute

### Step 6: Install Dependencies
On the Oracle VM (ssh terminal), run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y

# Install Docker Compose
sudo apt install docker-compose -y

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Verify
docker --version
```

✅ Docker installed!

### Step 7: Clone Repository
```bash
# Install git
sudo apt install git -y

# Clone your repo
git clone https://github.com/YOUR_USERNAME/employee-attendance-system.git
cd employee-attendance-system/backend
```

✅ Code cloned!

### Step 8: Create Environment File
```bash
# Create .env file
nano .env
```

Paste this (update values):
```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_DB_PASSWORD@attendance-db.subnets.oraclevcn.com:5432/postgres
JWT_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=https://YOUR_VERCEL_FRONTEND.vercel.app
```

**Save**: Press `Ctrl+X`, then `Y`, then `Enter`

✅ Environment configured!

### Step 9: Build and Run with Docker
```bash
# Build Docker image
docker build -t attendance-backend .

# Run container
docker run -d \
  --name attendance-backend \
  -p 8000:8000 \
  --env-file .env \
  attendance-backend

# Check if running
docker ps

# View logs
docker logs attendance-backend
```

✅ Backend is running!

### Step 10: Get Your Backend URL
Your backend is now at:
```
http://YOUR_PUBLIC_IP:8000
```

Example: `http://132.226.34.56:8000`

But we need HTTPS for Vercel CORS! 

---

## Phase 5: Set Up HTTPS with Nginx & Let's Encrypt

### Step 11: Install Nginx
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Step 12: Install SSL Certificate
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (interactive)
sudo certbot certonly --nginx -d YOUR_DOMAIN

# Or use a free domain: https://freedns.afraid.org/
# Then use: sudo certbot certonly --nginx -d your-subdomain.freedns.afraid.org
```

### Step 13: Configure Nginx Reverse Proxy
```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/default
```

Replace the content with:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name YOUR_DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

**Save**: `Ctrl+X`, `Y`, `Enter`

### Step 14: Enable SSL
```bash
# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Auto-redirect HTTP to HTTPS (optional but recommended)
sudo certbot renew --dry-run
```

✅ HTTPS is now active!

---

## Phase 6: Deploy Frontend to Vercel

### Step 15: Update Vercel Environment
1. Go to [vercel.com](https://vercel.com)
2. Select your project
3. Settings → Environment Variables
4. Update `NEXT_PUBLIC_API_URL`:
   - Old: `http://your-railway-url`
   - New: `https://YOUR_DOMAIN` (your Oracle instance domain)
5. Click "Save"
6. Go to Deployments → Click latest → "Redeploy"

✅ Frontend updated!

---

## Troubleshooting

### ❌ Can't connect to instance
- Check Security Lists allow port 22 (SSH)
- Check SSH key has correct permissions: `chmod 600 attendance-backend.key`
- Try different SSH key format

### ❌ Docker container exits
```bash
# Check logs
docker logs attendance-backend

# Restart
docker restart attendance-backend
```

### ❌ Database connection fails
- Verify database is AVAILABLE (green status)
- Check connection string format
- Test with psql: `psql -h attendance-db.subnets.oraclevcn.com -U postgres`

### ❌ CORS errors in browser
- Update `BACKEND_CORS_ORIGINS` to exact Vercel URL
- Restart container: `docker restart attendance-backend`

### ❌ API returns 500
- Check Docker logs: `docker logs attendance-backend`
- Verify DATABASE_URL is correct
- Check JWT_SECRET_KEY is set

---

## Monitoring & Management

### View Backend Logs
```bash
docker logs -f attendance-backend
```

### Restart Backend
```bash
docker restart attendance-backend
```

### Check Running Containers
```bash
docker ps
```

### Stop Backend
```bash
docker stop attendance-backend
```

### Start Backend Again
```bash
docker start attendance-backend
```

---

## Auto-Start on Reboot

To keep backend running if instance restarts:

```bash
# Create systemd service
sudo nano /etc/systemd/system/attendance-backend.service
```

Paste:
```ini
[Unit]
Description=Attendance Backend Service
After=docker.service
Requires=docker.service

[Service]
Type=simple
Restart=always
RestartSec=10
WorkingDirectory=/home/ubuntu/employee-attendance-system/backend
ExecStart=/usr/bin/docker start -a attendance-backend
ExecStop=/usr/bin/docker stop attendance-backend

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable attendance-backend.service
sudo systemctl start attendance-backend.service
```

---

## Final Verification

Test all these:

1. **Backend Health**:
   ```bash
   curl https://YOUR_DOMAIN/api/health
   # Response: {"status":"ok"}
   ```

2. **Frontend loads**: Open Vercel URL

3. **Login works**: Try to login in frontend

4. **API docs**: 
   ```
   https://YOUR_DOMAIN/docs
   ```

---

## URLs Summary

- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://YOUR_DOMAIN/`
- **API Docs**: `https://YOUR_DOMAIN/docs`
- **SSH**: `ssh -i key.pem ubuntu@YOUR_PUBLIC_IP`

---

## Cost

✅ **Everything free forever!**
- Compute: $0 (Always Free)
- Database: $0 (Always Free)
- Frontend: $0 (Vercel free tier)
- SSL: $0 (Let's Encrypt)

---

## Next Steps

1. Set up monitoring (optional)
2. Configure backups (automatic)
3. Add custom domain (optional)
4. Scale if needed (upgrade to paid)

🎉 You're deployed!
