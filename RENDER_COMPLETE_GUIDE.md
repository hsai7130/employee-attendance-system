# Render Deployment - Complete Reference

## Full Setup Guide

### What is Render?

Render is like Railway but:
- ✅ Truly free (free tier never expires)
- ✅ Automatic Docker builds
- ✅ Free PostgreSQL database
- ✅ Automatic GitHub deploys
- ✅ Simple web interface

### What You Get (Free)

- 1 free web service
- 1 free PostgreSQL database (90 days, then can recreate)
- Auto deploys from GitHub
- SSL certificates included
- 100GB data transfer/month

---

## Step-by-Step Detailed Guide

### 1. Sign Up (1 minute)

1. Go to https://render.com
2. Click "Get Started"
3. Sign in with GitHub
4. Authorize Render to access your GitHub repos
5. Accept Terms
6. Dashboard opens

✅ **Account created!**

---

### 2. Create PostgreSQL Database (2 minutes)

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"** from the menu
3. Fill in:
   - **Name**: `attendance-db`
   - **Database**: `postgres` (auto-filled)
   - **User**: `postgres` (auto-filled)
   - **Region**: Select closest to you
   - **PostgreSQL Version**: Latest (default)
4. Click **"Create Database"**

⏳ **Database is provisioning** - takes about 2 minutes

**While waiting**, open the database details page and find:
```
Internal Database URL
```

It looks like:
```
postgresql://postgres:YOUR_PASSWORD@dpg-xxx.render.internal/postgres
```

**Copy the entire URL and save it!**

---

### 3. Create Backend Web Service (2 minutes)

1. Back in Dashboard, click **"New +"** button again
2. Select **"Web Service"**
3. A page opens to connect repository
4. Find and select: `employee-attendance-system`
5. Click **"Connect"**

**Configure Service**:
- **Name**: `attendance-backend`
- **Region**: Same as database
- **Branch**: `main`
- **Runtime**: `Docker` (auto-detected)
- **Build Command**: (leave blank - uses Dockerfile)
- **Start Command**: (leave blank - uses Dockerfile)
- **Instance Type**: `Free` (default)

6. Click **"Create Web Service"**

⏳ **Building** - will show build logs on screen

---

### 4. Add Environment Variables (3 minutes)

While service is building, go to the service page:

1. Click on your backend service (from dashboard)
2. Scroll down to **"Environment"** section
3. Click **"Add Environment Variable"**

Add all 4 variables one by one:

**Variable 1: DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: (paste the Internal Database URL from Step 2)
  ```
  postgresql://postgres:PASSWORD@dpg-xxx.render.internal/postgres
  ```

**Variable 2: JWT_SECRET_KEY**
- **Key**: `JWT_SECRET_KEY`
- **Value**: 
  ```
  a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
  ```

**Variable 3: ACCESS_TOKEN_EXPIRE_MINUTES**
- **Key**: `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Value**: `30`

**Variable 4: BACKEND_CORS_ORIGINS**
- **Key**: `BACKEND_CORS_ORIGINS`
- **Value**: `https://your-vercel-project.vercel.app`
  - Replace `your-vercel-project` with your actual Vercel project name

After adding last variable, click outside or hit Tab.

Render auto-detects changes and **redeploys automatically**.

✅ **Environment variables saved!**

---

### 5. Wait for Build to Complete (3 minutes)

You'll see logs scrolling in the "Logs" section.

**Look for this message**:
```
Listening on http://0.0.0.0:8000
```

When you see it, your backend is running! ✅

In the top right, you'll see your service URL:
```
https://attendance-backend-xxxxx.onrender.com
```

**Copy and save this URL!**

---

### 6. Test Backend

Open in browser:
```
https://attendance-backend-xxxxx.onrender.com/api/health
```

Should return:
```json
{"status":"ok"}
```

✅ **Backend working!**

---

### 7. Update Vercel Frontend (2 minutes)

Go to https://vercel.com

1. Click your project: `employee-attendance-system`
2. Go to **Settings** → **Environment Variables**
3. Find `NEXT_PUBLIC_API_URL`
4. Update the value to your Render backend URL:
   ```
   https://attendance-backend-xxxxx.onrender.com
   ```
5. Click **"Save"**

6. Go to **Deployments** tab
7. Find your latest deployment
8. Click **"Redeploy"** button
9. Wait for redeploy to finish

✅ **Frontend updated!**

---

### 8. Final Testing (1 minute)

Test all three:

1. **Backend Health**:
   ```
   https://attendance-backend-xxxxx.onrender.com/api/health
   Response: {"status":"ok"}
   ```

2. **Frontend**:
   ```
   https://your-vercel-project.vercel.app
   Should load login page
   ```

3. **API Connection**:
   - Open frontend URL
   - Open DevTools: F12
   - Go to "Network" tab
   - Try to log in
   - Should see POST to `/api/auth/login` succeed

✅ **Everything working!**

---

## Important Details

### Database URL Format

Your database URL will be:
```
postgresql://postgres:YOUR_GENERATED_PASSWORD@dpg-abc123def456.render.internal/postgres
```

- **PostgreSQL** part is protocol
- **postgres:PASSWORD** is username and auto-generated password (don't change!)
- **@dpg-xxx.render.internal** is internal hostname (Render provides this)
- **postgres** is database name

**Don't try to change it** - use exactly as Render provides.

### Environment Variables Explained

| Variable | What it does | Example |
|----------|------------|---------|
| `DATABASE_URL` | Connects backend to database | `postgresql://...` |
| `JWT_SECRET_KEY` | Signs auth tokens (keep secret!) | `a1b2c3d4e5...` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | How long tokens last | `30` |
| `BACKEND_CORS_ORIGINS` | Allows frontend to call backend | `https://your-vercel-app.vercel.app` |

### Free Tier Limits

- **Web Service**: 1 free instance (unlimited)
- **Database**: 1 free PostgreSQL (90 days, then recreate)
- **Data Transfer**: 100GB/month
- **Compute**: Shared CPU (not dedicated)
- **Memory**: 512MB
- **Cold starts**: Yes (wakes up after 15 min inactivity)

### Auto-Deploys

After initial setup, every time you push to GitHub:
```bash
git push origin main
```

Render automatically:
1. Detects the push
2. Pulls latest code
3. Rebuilds Docker image
4. Deploys new version
5. Restarts container

No manual deploy needed! 🎉

---

## Troubleshooting

### Build Failed

**Check Logs**:
1. Go to service page
2. Scroll to "Logs" section
3. Look for red error messages

**Common fixes**:
- Make sure `backend/Dockerfile` exists
- Make sure `backend/pyproject.toml` exists
- Wait 5 min and click "Manual Deploy" button

### CORS Errors in Browser

**Fix**:
1. Go to Render backend service
2. Environment tab
3. Update `BACKEND_CORS_ORIGINS` to exact Vercel URL
4. Click outside to save
5. Render auto-redeploys (check Logs)
6. Clear browser cache (Ctrl+Shift+Delete)
7. Refresh frontend

### API Returns 500 Error

**Check**:
1. Render dashboard → service → Logs tab
2. Look for error messages
3. Common causes:
   - DATABASE_URL wrong
   - JWT_SECRET_KEY missing
   - Database not running

**Fix**:
1. Verify environment variables
2. Check database is "Available"
3. Click "Manual Deploy" in service

### Database Connection Refused

**Verify**:
1. In Render → PostgreSQL service → Status should be "Available"
2. DATABASE_URL format is correct
3. Try manual deploy

**Wait if**:
- Just created database (takes 2 min)
- Just updated env vars (Render is restarting)

---

## Monitoring

### Check Service Status
```
Render Dashboard → Your Service
Status shows at top (green = running)
```

### View Logs Live
```
Render Dashboard → Your Service → Logs tab
Shows real-time logs
```

### Check Environment Variables
```
Render Dashboard → Your Service → Environment tab
All variables listed here
```

### Manual Deploy
```
Render Dashboard → Your Service
"Manual Deploy" button (top right)
Rebuilds and redeploys immediately
```

---

## Security Notes

1. **Never commit .env files** to GitHub
2. **Keep JWT_SECRET_KEY secret** - don't share it
3. **Use Render's encrypted env variables** (automatic)
4. **Database password is auto-generated** - don't change it
5. **CORS_ORIGINS** should only be your Vercel URL

---

## Costs

✅ **Free Forever** until:
- Database reaches 90 days (then can recreate)
- You add paid services

When free tier expires on database:
- Option 1: Delete and recreate (free again)
- Option 2: Upgrade to paid ($15/month)

---

## Next Steps

1. ✅ Push any code changes with `git push origin main`
2. ✅ Render auto-redeploys
3. ✅ Monitor logs if something breaks
4. ✅ Before day 90: Plan database recreation

---

## Support

- **Render Docs**: https://docs.render.com/
- **Status Page**: https://status.render.com/
- **Support**: help@render.com

---

**Total Setup Time: ~10 minutes** ⏱️

**Status: ✅ DEPLOYED & LIVE**
