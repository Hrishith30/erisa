# Deployment Troubleshooting Guide

## 🔍 Current Issues

### 1. 400 Bad Request Error
**Symptoms**: Getting 400 Bad Request when accessing the application
**Possible Causes**:
- Database connection issues
- Missing environment variables
- Static files not loading properly
- Middleware conflicts

### 2. Login Page Not Redirecting
**Symptoms**: Login page doesn't redirect properly after authentication
**Possible Causes**:
- Custom middleware causing redirect loops
- Session configuration issues
- URL routing problems

## 🛠️ Solutions Applied

### 1. Fixed Database Configuration
```python
# Added try-catch for dj-database-url import
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL)
        }
    except ImportError:
        # Fallback to SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'claims.db',
            }
        }
```

### 2. Simplified Static Files Configuration
```python
# Changed from CompressedManifestStaticFilesStorage to CompressedStaticFilesStorage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
```

### 3. Temporarily Disabled Custom Middleware
```python
# Commented out to test if it's causing redirect loops
# 'claims_interface.middleware.AuthenticationMiddleware',
```

### 4. Added Health Check Endpoint
```python
def health_check(request):
    return JsonResponse({'status': 'healthy', 'message': 'Claims Management System is running'})
```

## 🔧 Testing Steps

### 1. Check Health Endpoint
```bash
curl https://your-app.onrender.com/health/
```
**Expected**: `{"status": "healthy", "message": "Claims Management System is running"}`

### 2. Check Root URL
```bash
curl -I https://your-app.onrender.com/
```
**Expected**: 302 redirect to `/login/`

### 3. Check Login URL
```bash
curl -I https://your-app.onrender.com/login/
```
**Expected**: 200 OK with login page

### 4. Check Static Files
```bash
curl -I https://your-app.onrender.com/static/css/style.css
```
**Expected**: 200 OK with CSS content

## 🚨 Common Issues and Fixes

### Issue 1: Database Connection Failed
**Error**: `django.db.utils.OperationalError`
**Solution**:
1. Check `DATABASE_URL` environment variable in Render
2. Ensure PostgreSQL service is running
3. Verify database credentials

### Issue 2: Static Files Not Found
**Error**: 404 for static files
**Solution**:
1. Run `python manage.py collectstatic --noinput`
2. Check `STATIC_ROOT` directory exists
3. Verify WhiteNoise configuration

### Issue 3: Import Error for dj-database-url
**Error**: `ModuleNotFoundError: No module named 'dj_database_url'`
**Solution**:
1. Ensure `dj-database-url==2.1.0` is in requirements.txt
2. Check if package is installed during build

### Issue 4: Redirect Loop
**Error**: Infinite redirects between login and dashboard
**Solution**:
1. Disable custom middleware temporarily
2. Check `LOGIN_REDIRECT_URL` setting
3. Verify authentication views

## 📋 Debug Checklist

### Pre-Deployment
- [ ] All files committed to Git
- [ ] `requirements.txt` updated
- [ ] `render.yaml` configured
- [ ] Environment variables set
- [ ] Database service created

### Post-Deployment
- [ ] Health endpoint responds
- [ ] Root URL redirects to login
- [ ] Login page loads
- [ ] Static files accessible
- [ ] Database migrations applied
- [ ] Admin user created

### Environment Variables Check
```bash
# In Render dashboard, verify these are set:
SECRET_KEY = (auto-generated)
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = (from PostgreSQL service)
```

## 🔄 Next Steps

1. **Deploy with current fixes**
2. **Test health endpoint**: `https://your-app.onrender.com/health/`
3. **Test login page**: `https://your-app.onrender.com/login/`
4. **If issues persist, check Render logs**
5. **Re-enable middleware if login works**

## 📞 Getting Help

### Render Logs
- Check build logs for errors
- Check runtime logs for exceptions
- Monitor health check failures

### Django Debug
```bash
# Enable debug temporarily
DEBUG = True
```

### Manual Testing
1. Visit health endpoint
2. Try login with admin/admin123
3. Check if dashboard loads
4. Test static files

---

**Status**: Fixed database config, simplified static files, disabled problematic middleware
**Next**: Deploy and test health endpoint
