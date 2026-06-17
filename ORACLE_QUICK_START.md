# Oracle Cloud Deployment - 15 Minute Quick Start

## ⚡ TLDR - Do This Now

### 1️⃣ Create Oracle Cloud Account (2 min)
```
Go to: https://www.oracle.com/cloud/free/
→ Click "Start for free"
→ Sign up with email
→ Verify email
→ Done!
```

✅ **Account created**

---

### 2️⃣ Create PostgreSQL Database (2 min setup + 10 min wait)
In Oracle Cloud Console:
```
☰ Menu → Databases → PostgreSQL
→ "Create DB System"
→ Name: attendance-db
→ Password: ChooseStrongPassword123!
→ Keep other settings default
→ Click "Create"
⏳ Wait for "AVAILABLE" status (5-10 min)
```

**Save your DB credentials**:
```
Host: attendance-db.subnets.oraclevcn.com
Port: 5432
User: postgres
Password: ChooseStrongPassword123!
```

✅ **Database created**

---

### 3️⃣ Create Compute Instance (2 min setup + 3 min wait)
In Oracle Cloud Console:
```
☰ Menu → Compute → Instances
→ "Create Instance"
→ Name: attendance-backend
→ Image: Ubuntu 22.04 (free)
→ Shape: Ampere (free tier)
→ SSH Key: Download and save!
→ Public IP: Enabled ✓
→ Click "Create"
⏳ Wait for "RUNNING" status
```

**Save your SSH key!** (download appears immediately)

✅ **Compute instance created**

---

### 4️⃣ Connect to Your Instance (1 min)
```powershell
# In PowerShell where you saved SSH key:
cd Downloads

# Connect (replace with your PUBLIC_IP from Oracle Console)
ssh -i attendance-backend.key ubuntu@YOUR_PUBLIC_IP

# Type 'yes' when asked
```

✅ **Connected to Oracle VM**

---

### 5️⃣ Install Docker & Deploy Backend (3 min)
Run these commands on the Oracle VM:

```bash
# Install Docker
sudo apt update && sudo apt install docker.io docker-compose -y

# Add user to docker group
sudo usermod -aG docker ubuntu && newgrp docker

# Clone your repo
git clone https://github.com/YOUR_USERNAME/employee-attendance-system.git
cd employee-attendance-system/backend

# Create environment file
cat > .env << 'EOF'
DATABASE_URL=postgresql+psycopg://postgres:ChooseStrongPassword123!@attendance-db.subnets.oraclevcn.com:5432/postgres
JWT_SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=https://YOUR-VERCEL-PROJECT.vercel.app
EOF

# Build and run
docker build -t attendance-backend .
docker run -d --name attendance-backend -p 8000:8000 --env-file .env attendance-backend

# Check status
docker ps
```

**Replace these**:
- `ChooseStrongPassword123!` → your DB password from step 2
- `YOUR_USERNAME` → your GitHub username
- `YOUR-VERCEL-PROJECT` → your Vercel project name

✅ **Backend running!**

---

### 6️⃣ Get Public URL (1 min)
From Oracle Console:
```
Copy your instance's PUBLIC_IP_ADDRESS

Your backend is now at:
http://YOUR_PUBLIC_IP:8000/api/health

Should return: {"status":"ok"}
```

---

### 7️⃣ Update Vercel (1 min)
Go to Vercel project → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL = http://YOUR_PUBLIC_IP:8000
```

Then: Deployments → Redeploy latest

✅ **Connected!**

---

## ✅ Verify It Works

Test in browser:
1. **Backend health**: `http://YOUR_PUBLIC_IP:8000/api/health`
2. **Frontend**: Your Vercel URL
3. **Try login**: See Network tab requests succeed

---

## 🎉 Done!

Your app is now running:
- **Frontend**: On Vercel (free)
- **Backend**: On Oracle Cloud (free forever)
- **Database**: On Oracle Cloud (free forever)

---

## ⚠️ Important Notes

1. **Keep SSH key safe** - don't share it
2. **Save DB password** - you'll need it later
3. **Note your Public IP** - it's your backend URL
4. **Database takes 10 min** - be patient
5. **HTTP for now** - HTTPS setup in detailed guide

---

## 🆘 If Something Goes Wrong

### Can't SSH in?
```
- Wait 5 min after instance shows RUNNING
- Check SSH key permissions: chmod 600 key.pem
- Verify Public IP is copied correctly
```

### Backend not accessible?
```
- Wait 1 min after docker run command
- Check: docker ps (should show container running)
- Check logs: docker logs attendance-backend
```

### API returning errors?
```
- Check DATABASE_URL is correct
- Check backend logs: docker logs -f attendance-backend
- Verify database shows "AVAILABLE" status
```

---

## 📖 Full Details

For SSL setup, monitoring, and advanced config:
👉 Read [ORACLE_CLOUD_SETUP.md](ORACLE_CLOUD_SETUP.md)

---

**Go deploy! 🚀**
