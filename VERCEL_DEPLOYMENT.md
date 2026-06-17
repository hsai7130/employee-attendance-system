# Vercel Deployment Guide

This guide covers deploying the **frontend to Vercel** and the **backend to a separate service**.

## Part 1: Deploy Frontend to Vercel

### Step 1: Connect GitHub Repository
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub (or create an account)
3. Click "Add New" → "Project"
4. Select your `employee-attendance-system` repository
5. Click "Import"

### Step 2: Configure Project Settings
- **Project Name**: `employee-attendance-system` (or your choice)
- **Framework Preset**: Next.js (should auto-detect)
- **Root Directory**: `frontend`

### Step 3: Environment Variables
Add these in Vercel Project Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL = https://your-backend-api.com
```

**Important**: Replace `https://your-backend-api.com` with your actual backend URL (see Part 2).

### Step 4: Deploy
Click "Deploy" and wait for the build to complete.

Your frontend will be available at: `https://your-project.vercel.app`

---

## Part 2: Deploy Backend Separately

Since Vercel doesn't support Python/FastAPI natively, choose one of these options:

### Option A: Railway (Recommended - Easiest)
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will auto-detect FastAPI
5. Configure environment variables:
   ```
   DATABASE_URL=postgresql+psycopg://user:password@host:port/dbname
   JWT_SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   BACKEND_CORS_ORIGINS=https://your-project.vercel.app
   ```
6. Deploy (Railway handles Docker automatically)

Your backend will be at: `https://your-project.up.railway.app`

### Option B: Render
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configuration:
   - **Environment**: Docker
   - **Build Command**: (auto-detected)
   - **Start Command**: (auto-detected)
5. Add environment variables (same as Railway)

### Option C: Heroku (Requires Credit Card)
1. Go to [heroku.com](https://heroku.com)
2. Create account and add payment method
3. Create new app
4. Connect GitHub and select repository
5. Enable automatic deploys
6. Add environment variables in Settings

---

## Part 3: Update Frontend to Use Backend URL

After deploying the backend, update the `NEXT_PUBLIC_API_URL` in Vercel:

1. Go to Vercel Project Settings
2. Find "Environment Variables"
3. Update `NEXT_PUBLIC_API_URL` to your backend URL
4. Trigger a new deployment (redeploy your project)

---

## Environment Variables Checklist

### Frontend (Vercel)
- [ ] `NEXT_PUBLIC_API_URL` - Backend URL

### Backend (Railway/Render/Heroku)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `JWT_SECRET_KEY` - Strong secret key (generate with `openssl rand -hex 32`)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry (e.g., 30)
- [ ] `BACKEND_CORS_ORIGINS` - Frontend URL (e.g., `https://your-project.vercel.app`)

---

## Database Setup

For the PostgreSQL database, you can:
1. Use the database provided by Railway/Render/Heroku (easiest)
2. Use AWS RDS or Azure Database for PostgreSQL
3. Use Supabase (PostgreSQL hosting) at [supabase.com](https://supabase.com)

---

## Production Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Set `BACKEND_CORS_ORIGINS` to your Vercel frontend URL only
- [ ] Enable HTTPS (automatic with Vercel and most services)
- [ ] Set up database backups
- [ ] Configure monitoring/logging
- [ ] Test login and API calls end-to-end
- [ ] Update your Vercel environment variables with production backend URL

---

## Testing After Deployment

1. Open your Vercel frontend URL
2. Test login functionality (calls `/api/auth/login`)
3. Test employee list page (calls `/api/employees`)
4. Check browser console for any CORS errors

---

## Troubleshooting

### CORS Errors
- Ensure `BACKEND_CORS_ORIGINS` includes your Vercel frontend URL
- Restart backend service after changing this

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is correct in Vercel
- Check network tab in browser DevTools
- Ensure backend is running and healthy

### Database Connection Issues
- Verify `DATABASE_URL` format is correct
- Test connection string locally first
- Check if PostgreSQL service is running

---

## Security Tips

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use strong JWT secrets** - Generate with: `openssl rand -hex 32`
3. **Rotate secrets periodically**
4. **Use Vercel's encrypted environment variables**
5. **Enable branch protection** on GitHub main branch
6. **Use HTTPS only** in production
