# Quick Deployment Checklist - Vercel + Backend

## Phase 1: Frontend to Vercel (10 minutes)

### Prerequisites
- GitHub account
- Vercel account (free)
- Your repo pushed to GitHub

### Steps
1. [ ] Go to [vercel.com](https://vercel.com) → Sign in with GitHub
2. [ ] Click "Add New" → "Project"
3. [ ] Select `employee-attendance-system` repository
4. [ ] Framework: **Next.js** (auto-detected)
5. [ ] Root Directory: **frontend**
6. [ ] Click "Deploy"
7. [ ] Wait for deployment to complete
8. [ ] Note your Vercel URL: `https://your-project.vercel.app`

**Status**: ✅ Frontend deployed (but API calls will fail without backend)

---

## Phase 2: Backend Deployment (Choose One)

### Option A: Railway (Recommended - Easiest)
1. [ ] Go to [railway.app](https://railway.app)
2. [ ] Sign in with GitHub
3. [ ] Click "New Project" → "Deploy from GitHub repo"
4. [ ] Select your repository
5. [ ] Select `backend` as root directory
6. [ ] Railway auto-creates PostgreSQL database
7. [ ] Go to "Variables" tab
8. [ ] Add variables:
   ```
   JWT_SECRET_KEY=<generate-with-command-below>
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   BACKEND_CORS_ORIGINS=https://your-project.vercel.app
   DATABASE_URL=<Railway auto-generates this>
   ```
9. [ ] Deploy button (Railway deploys automatically)
10. [ ] Note your Railway URL from deployment info

**Generate JWT Secret:**
```powershell
# Windows PowerShell
$bytes = [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
[System.BitConverter]::ToString($bytes).Replace("-", "").ToLower()
```

### Option B: Render
1. [ ] Go to [render.com](https://render.com)
2. [ ] Sign in with GitHub
3. [ ] New Web Service
4. [ ] Select repository → `backend` folder
5. [ ] Environment: Docker
6. [ ] Add same environment variables as Railway
7. [ ] For database: Add PostgreSQL service
8. [ ] Deploy

### Option C: Heroku
1. [ ] Go to [heroku.com](https://heroku.com)
2. [ ] Add payment method (required now)
3. [ ] Create new app
4. [ ] Connect GitHub, select repository
5. [ ] Add Heroku Postgres add-on
6. [ ] Add environment variables
7. [ ] Enable automatic deploys

**Status**: ✅ Backend deployed

---

## Phase 3: Connect Frontend to Backend

### Update Vercel Environment Variables
1. [ ] Go to Vercel Project → Settings → Environment Variables
2. [ ] Find `NEXT_PUBLIC_API_URL`
3. [ ] Update value to your backend URL:
   - Railway: `https://your-project.up.railway.app`
   - Render: `https://your-project.onrender.com`
   - Heroku: `https://your-project.herokuapp.com`
4. [ ] **Redeploy** the frontend (Vercel → Deployments → Click latest)

**Status**: ✅ Frontend & Backend connected

---

## Phase 4: Testing

### Test Frontend
1. [ ] Open `https://your-project.vercel.app`
2. [ ] Should load without errors

### Test Backend Health
```powershell
curl https://your-backend-url/api/health
# Response: {"status":"ok"}
```

### Test Login
1. [ ] On frontend, try to log in
2. [ ] Check browser DevTools → Network tab
3. [ ] Should see successful request to `/api/auth/login`
4. [ ] No CORS errors

---

## Common Issues & Fixes

### ❌ "Cannot read properties of undefined" on frontend
- Backend URL is wrong in `NEXT_PUBLIC_API_URL`
- Solution: Update in Vercel → Environment Variables → Redeploy

### ❌ CORS error: "Access to XMLHttpRequest blocked"
- `BACKEND_CORS_ORIGINS` doesn't match your Vercel URL
- Solution: Update backend env var → Redeploy backend

### ❌ Login keeps redirecting to login page
- `JWT_SECRET_KEY` might be wrong or empty
- Solution: Set JWT_SECRET_KEY in backend vars → Redeploy

### ❌ 500 error on login
- Database connection failed
- Check `DATABASE_URL` format is correct
- Test database is running on hosting service

---

## Environment Variables Reference

### Frontend (`NEXT_PUBLIC_API_URL`)
- Local: `http://localhost:8000`
- Production: `https://your-backend.xyz`

### Backend (All Required)
```
DATABASE_URL = postgresql+psycopg://user:pass@host:port/db
JWT_SECRET_KEY = [32-char random hex string]
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BACKEND_CORS_ORIGINS = https://your-vercel-app.vercel.app
```

---

## Final Verification

- [ ] Frontend loads at Vercel URL
- [ ] Backend health check returns `{"status":"ok"}`
- [ ] Login page is accessible
- [ ] Login API call succeeds (check DevTools Network)
- [ ] No CORS errors in console
- [ ] Employee list page loads data from API

---

## Database Backups

- **Railway**: Automatic daily backups
- **Render**: Backup policy in settings
- **Heroku**: Add Heroku Postgres backup add-on

---

## Next Steps

1. Add more API integration to frontend components
2. Set up monitoring/alerts
3. Configure custom domain (optional)
4. Set up CI/CD for automatic deployments
5. Add logging & error tracking (e.g., Sentry)
