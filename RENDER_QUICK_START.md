# Render Deployment - 10 Minute Setup

## 🎯 QUICK STEPS - Just Follow Exactly

### STEP 1: Create Render Account (1 min)
```
https://render.com
→ "Get Started" button
→ Sign in with GitHub
→ Authorize render-examples
✅ Done!
```

---

### STEP 2: Create PostgreSQL Database (1 min)
In Render Dashboard:
```
Click "New +" button (top right)
→ Select "PostgreSQL"
→ Name: attendance-db
→ Database: postgres
→ User: postgres
→ Region: Closest to you
→ Keep other defaults
→ "Create Database"
```

⏳ **Database is provisioning (~2 min)**

**While waiting**, copy your Internal Database URL from database page:
```
postgresql://postgres:PASSWORD@dpg-xxx.render.internal/postgres
```

**SAVE THIS!**

---

### STEP 3: Create Backend Service (2 min)
Still in Render Dashboard:
```
Click "New +" button
→ Select "Web Service"
→ Connect "employee-attendance-system" repo from GitHub
→ Select repository
→ Continue
```

**Configure**:
```
Name: attendance-backend
Environment: Docker
Build Command: (leave default)
Start Command: (leave default)
Instance Type: Free (default)
→ "Create Web Service"
```

⏳ **Backend is building (~3-4 min)**

---

### STEP 4: Add Environment Variables (2 min)
Still building? Go to your backend service → "Environment" tab

Click "Add Environment Variable" and add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres:PASSWORD@dpg-xxx.render.internal/postgres` |
| `JWT_SECRET_KEY` | `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `BACKEND_CORS_ORIGINS` | `https://YOUR-VERCEL-PROJECT.vercel.app` |

**REPLACE:**
- `postgresql://postgres:PASSWORD@dpg-xxx.render.internal/postgres` → Paste from Step 2
- `YOUR-VERCEL-PROJECT` → Your Vercel project name

**Click "Save"** → Render auto-redeploys ✅

---

### STEP 5: Wait for Build & Get URL (3 min)
In Render Dashboard:
```
Watch "Logs" tab
Wait for "Listening on http://0.0.0.0:8000"
```

Once done, copy your backend URL from top:
```
https://attendance-backend-xxxxx.onrender.com
```

**Test it**:
```
https://attendance-backend-xxxxx.onrender.com/api/health
Should return: {"status":"ok"}
```

✅ **Backend live!**

---

### STEP 6: Update Vercel (1 min)
Go to [vercel.com](https://vercel.com):
```
Your Project → Settings → Environment Variables
Find: NEXT_PUBLIC_API_URL
Update to: https://attendance-backend-xxxxx.onrender.com
Click "Save"
```

Then:
```
Go to Deployments tab
Click "Redeploy" on latest deployment
Wait for completion
```

✅ **Connected!**

---

## ✅ DONE! Verify It Works

Open these in browser:

1. **Backend health**: `https://attendance-backend-xxxxx.onrender.com/api/health`
   - Should show: `{"status":"ok"}`

2. **Your frontend**: `https://your-vercel-project.vercel.app`
   - Should load login page

3. **Try login**:
   - DevTools (F12) → Network tab
   - Click login
   - Should see successful `/api/auth/login` request

---

## 🎉 YOU'RE DEPLOYED!

**Your URLs:**
- Frontend: `https://your-vercel-project.vercel.app`
- Backend: `https://attendance-backend-xxxxx.onrender.com`
- API Docs: `https://attendance-backend-xxxxx.onrender.com/docs`

**Cost**: $0 (free tier)

---

## ⚠️ Important Notes

1. Render free tier has cold starts (~30s first request after 15 min inactivity)
2. Database is **free but only 90 days** - upgrade or recreate before day 90
3. Backend auto-deploys when you push to GitHub main branch
4. Frontend auto-redeploys on Vercel

---

## If Something Goes Wrong

### ❌ Build failed on Render
```
Check "Logs" tab for error
Common: Missing Dockerfile → It exists, wait and retry
Solution: Redeploy manually
```

### ❌ CORS error in browser
```
Update BACKEND_CORS_ORIGINS to exact Vercel URL
Redeploy Render backend
```

### ❌ 500 error on login
```
Check DATABASE_URL is correct
Check all env vars are set
Redeploy
```

---

## Useful Render Commands

**Redeploy manually**:
```
Render Dashboard → Backend Service → Manual Deploy button
```

**View logs live**:
```
Render Dashboard → Backend Service → Logs tab
```

**Check environment vars**:
```
Render Dashboard → Backend Service → Environment tab
```

---

## Next Deploys (After This)

Just push to GitHub:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically rebuilds and redeploys! 🎉

---

**TOTAL TIME: ~10 minutes ⏱️**

**Status: ✅ LIVE**
