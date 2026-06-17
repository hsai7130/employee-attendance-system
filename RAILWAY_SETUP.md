# Railway Deployment - Complete Setup Guide

## Step-by-Step Railway Deployment

### Phase 1: Set Up Railway Account & Project

#### 1. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Start Free" (top right)
3. Sign in with GitHub (click GitHub button)
4. Authorize railway-app to access your GitHub account
5. Done! You're now in the Railway dashboard

#### 2. Create New Project
1. Click "New Project" (in dashboard)
2. Select "Deploy from GitHub repo"
3. Find and select: `employee-attendance-system`
4. Railway starts connecting to your repo

---

### Phase 2: Configure Backend Service

#### 3. Select Backend Folder
1. You'll see "Select a template" - click "Skip"
2. You'll see your repo files - select the `backend` folder
3. Click "Create Service"
4. Railway starts building your backend from Docker

**Status**: Backend is building (this takes 2-3 minutes)

---

### Phase 3: Add Database

#### 4. Create PostgreSQL Database
1. In your Railway project, click "Create" → "Database" → "PostgreSQL"
2. Railway automatically creates a PostgreSQL instance
3. This links automatically to your backend service
4. **Important**: Railway auto-generates `DATABASE_URL` environment variable

**Status**: PostgreSQL is ready

---

### Phase 4: Set Environment Variables

#### 5. Configure Backend Environment Variables

In the Railway dashboard:
1. Click your **Backend** service card (should show FastAPI)
2. Click "Variables" tab
3. Click "Add Variable" and add these one by one:

**Variable 1: JWT_SECRET_KEY**
- **Key**: `JWT_SECRET_KEY`
- **Value**: Copy from below ⬇️

```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```
(This is a sample - Railway will use this as-is)

**Variable 2: ACCESS_TOKEN_EXPIRE_MINUTES**
- **Key**: `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Value**: `30`

**Variable 3: BACKEND_CORS_ORIGINS**
- **Key**: `BACKEND_CORS_ORIGINS`
- **Value**: `https://your-vercel-frontend.vercel.app`
(Replace `your-vercel-frontend` with your actual Vercel project name)

**Note**: Railway automatically provides `DATABASE_URL` - you don't need to add it!

4. Click "Deploy" or Railway auto-deploys after variable changes

**Status**: Backend environment configured ✅

---

### Phase 5: Get Your Backend URL

#### 6. Copy Backend URL
1. In Railway dashboard, click your Backend service
2. Look for "Deployments" section
3. You'll see a URL like: `https://employee-attendance-backend-production-xxxx.up.railway.app`
4. **Copy this URL** - you'll need it for Vercel

**Example**: `https://employee-attendance-production-1234.up.railway.app`

---

### Phase 6: Deploy Frontend to Vercel

#### 7. Update Vercel with Backend URL
1. Go to [vercel.com](https://vercel.com)
2. Click your project: `employee-attendance-system`
3. Go to Settings → Environment Variables
4. Find `NEXT_PUBLIC_API_URL`
5. Update to: (paste your Railway backend URL from Step 6)
6. Click "Save"
7. Go to Deployments tab
8. Click "Redeploy" on the latest deployment
9. Wait for redeploy to complete

**Status**: Frontend now connected to backend ✅

---

## Testing Your Deployment

### Test 1: Backend Health Check
```
Open in browser or curl:
https://your-railway-backend-url/api/health

Expected response: {"status":"ok"}
```

### Test 2: Frontend Load
```
Open: https://your-vercel-frontend.vercel.app

Should load without errors
```

### Test 3: Login API Call
1. Open your Vercel frontend
2. Open browser DevTools (F12)
3. Go to Network tab
4. Try to log in
5. Should see POST request to `/api/auth/login`
6. Response should include `access_token`

---

## Troubleshooting

### ❌ Build fails on Railway
**Error**: "Docker build failed" or "requirements.txt not found"
**Solution**: 
- Check `backend/Dockerfile` exists
- Check `backend/pyproject.toml` exists
- Restart the build in Railway dashboard

### ❌ API returns 500 error
**Error**: "Internal Server Error" when calling API
**Solution**:
- Check Database URL is correct (Railway → Backend → Variables)
- Restart backend service (Railway → Redeploy)

### ❌ CORS error in browser console
**Error**: "Access to XMLHttpRequest blocked by CORS policy"
**Solution**:
- Update `BACKEND_CORS_ORIGINS` to your Vercel URL
- Make sure Vercel URL is exactly: `https://your-project.vercel.app`
- Restart backend (Railway → Redeploy)

### ❌ 404 when calling API
**Error**: "Cannot POST /api/auth/login"
**Solution**:
- Check `NEXT_PUBLIC_API_URL` in Vercel is correct
- Redeploy Vercel frontend
- Verify backend URL format (should start with https://)

### ❌ Database connection error
**Error**: "could not connect to server: Connection refused"
**Solution**:
- Railway → PostgreSQL service → check status is "Running"
- In Backend variables, ensure `DATABASE_URL` is present
- Restart backend service

---

## URLs to Remember

After deployment, you'll have:

- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-project-production-xxxx.up.railway.app`
- **API Docs**: `https://your-project-production-xxxx.up.railway.app/docs`

---

## Environment Variables Checklist

### Railway Backend
- ✅ `DATABASE_URL` - Auto-provided by Railway
- ✅ `JWT_SECRET_KEY` - `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2`
- ✅ `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
- ✅ `BACKEND_CORS_ORIGINS` - `https://your-vercel-frontend.vercel.app`

### Vercel Frontend
- ✅ `NEXT_PUBLIC_API_URL` - `https://your-railway-backend.up.railway.app`

---

## Important Notes

1. **Never share your JWT_SECRET_KEY** in public repos or with others
2. **Keep your backend URL secret** (it's your API endpoint)
3. **Railway automatically handles**:
   - Docker builds
   - HTTPS certificates
   - Database backups
4. **Database URL**:
   - Automatically created and injected by Railway
   - You don't need to create or configure it manually

---

## Next Steps After Deployment

1. ✅ Test all pages in Vercel frontend
2. ✅ Test employee list, attendance, payroll pages
3. ✅ Test API endpoints with Postman if needed
4. ✅ Set up monitoring (Railway has built-in logs)
5. ✅ Add custom domain (optional, Railway allows this)
6. ✅ Configure email notifications for errors
7. ✅ Set up backups (automatic on Railway)

---

## Useful Railway Commands

### View Backend Logs
1. Railway dashboard → Backend service
2. Click "Logs" tab
3. See real-time deployment logs

### Check Environment Variables
1. Railway dashboard → Backend service
2. Click "Variables" tab
3. All configured variables shown here

### Restart Service
1. Railway dashboard → Backend service
2. Click "Deploy" → "Redeploy"
3. Service restarts with latest code

---

## GitHub Integration

Railway automatically:
- Watches your GitHub repo for changes
- Rebuilds when you push to `main` branch
- Deploys automatically after successful build
- Shows deployment status on GitHub (check branch for ✅/❌)

No additional GitHub Actions needed! 🎉
