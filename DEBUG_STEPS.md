# Debug Steps for 400 Bad Request Error

## 🔍 Step-by-Step Debugging

### Step 1: Check if the app is deploying at all

1. **Go to your Render dashboard**
2. **Check the build logs** - Look for any errors during build
3. **Check the runtime logs** - Look for any errors when the app starts

### Step 2: Test the health endpoint

After deployment, try these URLs in order:

1. **Health check**: `https://your-app.onrender.com/health/`
   - Should return: `{"status": "healthy", "message": "Claims Management System is running", ...}`

2. **Debug info**: `https://your-app.onrender.com/debug/`
   - Should return configuration information

3. **Root URL**: `https://your-app.onrender.com/`
   - Should redirect to login page

### Step 3: Check environment variables

In your Render dashboard, verify these environment variables are set:

```
SECRET_KEY = (should be auto-generated)
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = (should be provided by PostgreSQL service)
```

### Step 4: Test locally first

Run this locally to test basic setup:

```bash
python test_basic.py
```

### Step 5: Check specific issues

#### Issue A: Database Connection
**Symptoms**: 500 errors, database-related errors in logs
**Test**: Visit `/debug/` endpoint
**Fix**: Check DATABASE_URL in Render environment variables

#### Issue B: Static Files
**Symptoms**: CSS/JS not loading, 404 for static files
**Test**: Visit `/static/css/style.css`
**Fix**: Check if static files are collected during build

#### Issue C: Import Errors
**Symptoms**: ModuleNotFoundError in logs
**Test**: Check build logs for import errors
**Fix**: Verify all packages in requirements.txt

#### Issue D: URL Routing
**Symptoms**: 404 for all URLs
**Test**: Try `/health/` endpoint
**Fix**: Check urls.py configuration

## 🚨 Common 400 Error Causes

### 1. CSRF Token Issues
- **Cause**: Missing or invalid CSRF token
- **Fix**: Check if CSRF middleware is enabled

### 2. Database Connection Issues
- **Cause**: Cannot connect to PostgreSQL
- **Fix**: Verify DATABASE_URL and database service

### 3. Static Files Issues
- **Cause**: Static files not collected or served
- **Fix**: Check WhiteNoise configuration

### 4. Environment Variables
- **Cause**: Missing required environment variables
- **Fix**: Check all environment variables in Render

## 🔧 Quick Fixes to Try

### Fix 1: Enable Debug Mode Temporarily
In Render environment variables, set:
```
DEBUG = True
```

### Fix 2: Use SQLite Instead of PostgreSQL
Comment out the DATABASE_URL check in settings.py temporarily

### Fix 3: Disable All Custom Middleware
Comment out all custom middleware in settings.py

### Fix 4: Simplify Static Files
Change to:
```python
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
```

## 📋 Testing Checklist

- [ ] Build completes successfully
- [ ] Health endpoint responds
- [ ] Debug endpoint shows configuration
- [ ] Root URL redirects properly
- [ ] Login page loads
- [ ] Static files accessible
- [ ] Database migrations run
- [ ] Admin user created

## 🆘 If Still Getting 400 Error

1. **Check Render logs** for specific error messages
2. **Enable DEBUG=True** temporarily to see detailed errors
3. **Test with minimal settings** using settings_minimal.py
4. **Check if it's a specific URL** or all URLs
5. **Verify the app is actually running** (not just building)

## 📞 Next Steps

1. **Deploy the updated code** with debug endpoints
2. **Test the health endpoint** first
3. **Check the debug endpoint** for configuration info
4. **Share the specific error messages** from Render logs
5. **Try the quick fixes** one by one

---

**Remember**: The 400 error usually means the request is malformed or the server can't process it. This often indicates a configuration issue rather than a code issue.
