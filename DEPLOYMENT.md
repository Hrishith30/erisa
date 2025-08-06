# Deployment Guide for Claims Management System

This guide will help you deploy your Django Claims Management System to Render.

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository

Make sure your code is in a Git repository (GitHub, GitLab, etc.) with all the files we've created:

- `render.yaml` - Render configuration
- `requirements.txt` - Python dependencies
- `build.sh` - Build script
- Updated `settings.py` - Production settings
- Error templates (403.html, 400.html)

### 2. Deploy to Render

#### Option A: Using Render Dashboard (Recommended)

1. **Sign up/Login to Render**
   - Go to [render.com](https://render.com)
   - Sign up or login to your account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository
   - Select your repository

3. **Configure the Service**
   - **Name**: `claims-management-system`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn claims_interface.wsgi:application`
   - **Plan**: Free

4. **Environment Variables**
   Add these environment variables in the Render dashboard:
   ```
   SECRET_KEY = (Render will generate this automatically)
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   DATABASE_URL = (Render will provide this from the database service)
   ```

5. **Create Database**
   - Go to "New +" → "PostgreSQL"
   - Name: `claims-db`
   - Plan: Free
   - Copy the `DATABASE_URL` and add it to your web service environment variables

#### Option B: Using render.yaml (Blue/Green Deployment)

1. **Push your code** with the `render.yaml` file
2. **Connect repository** to Render
3. **Render will automatically** create both the web service and database

### 3. Initial Setup

After deployment, your app will be available at:
`https://your-app-name.onrender.com`

**Default Login Credentials:**
- Username: `admin`
- Password: `admin123`

**Important:** Change these credentials immediately after first login!

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Auto-generated |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts | `.onrender.com` |
| `DATABASE_URL` | Database connection | Auto-provided |
| `WEB_CONCURRENCY` | Gunicorn workers | `4` |

### Database Migration

The build script automatically:
1. Installs dependencies
2. Collects static files
3. Runs database migrations
4. Sets up initial data and admin user

### Static Files

Static files are served by WhiteNoise and automatically collected during build.

## 📊 Monitoring Your Deployment

### Health Checks
- **Health Check Path**: `/dashboard/`
- **Expected Response**: 200 OK
- **Check Frequency**: Every 30 seconds

### Logs
- Access logs in Render dashboard
- Monitor for errors and performance issues
- Set up alerts for critical errors

## 🔒 Security Considerations

### Production Security
- ✅ HTTPS enabled automatically
- ✅ Security headers configured
- ✅ CSRF protection enabled
- ✅ SQL injection protection
- ✅ XSS protection

### Admin Access
1. **Change default credentials** immediately
2. **Create new admin user**:
   ```bash
   python manage.py createsuperuser
   ```
3. **Delete default admin** if needed

### Environment Variables
- Never commit sensitive data to Git
- Use Render's environment variable system
- Rotate secrets regularly

## 🛠️ Troubleshooting

### Common Issues

#### 1. Build Failures
**Symptoms**: Build fails during deployment
**Solutions**:
- Check `requirements.txt` for missing dependencies
- Verify Python version compatibility
- Check build logs for specific errors

#### 2. Database Connection Issues
**Symptoms**: 500 errors, database connection failures
**Solutions**:
- Verify `DATABASE_URL` is set correctly
- Check database service is running
- Ensure migrations are applied

#### 3. Static Files Not Loading
**Symptoms**: CSS/JS not loading, broken styling
**Solutions**:
- Verify `collectstatic` ran successfully
- Check WhiteNoise configuration
- Ensure static files are in correct location

#### 4. Authentication Issues
**Symptoms**: Can't login, authentication errors
**Solutions**:
- Verify admin user was created
- Check login URL configuration
- Ensure session middleware is enabled

### Debug Commands

#### Check Application Status
```bash
# Check if app is responding
curl https://your-app.onrender.com/dashboard/

# Check health endpoint
curl https://your-app.onrender.com/dashboard/
```

#### Database Verification
```bash
# Connect to database and check tables
python manage.py dbshell
```

#### Static Files Check
```bash
# Verify static files are collected
python manage.py collectstatic --dry-run
```

## 📈 Performance Optimization

### Render Free Tier Limits
- **Build Time**: 45 minutes max
- **Request Timeout**: 30 seconds
- **Sleep Mode**: App sleeps after 15 minutes of inactivity
- **Bandwidth**: 750 GB/month

### Optimization Tips
1. **Use CDN** for static files (optional)
2. **Optimize images** and assets
3. **Enable caching** where possible
4. **Monitor performance** regularly

## 🔄 Updates and Maintenance

### Updating Your Application
1. **Push changes** to your Git repository
2. **Render automatically** detects changes
3. **Builds and deploys** automatically
4. **Health checks** verify deployment

### Database Backups
- Render provides automatic backups
- Access backups in Render dashboard
- Download backups for local development

### Monitoring
- Set up alerts for critical errors
- Monitor response times
- Track database performance
- Watch for memory usage

## 🆘 Support

### Render Support
- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Status](https://status.render.com)

### Django Support
- [Django Documentation](https://docs.djangoproject.com)
- [Django Community](https://www.djangoproject.com/community/)

### Application-Specific Issues
- Check the application logs in Render dashboard
- Review Django error logs
- Test locally before deploying

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] All code committed to Git
- [ ] `requirements.txt` updated
- [ ] `render.yaml` configured
- [ ] Environment variables set
- [ ] Database service created
- [ ] Static files configured

### Post-Deployment
- [ ] Application accessible via URL
- [ ] Health checks passing
- [ ] Admin login working
- [ ] Database migrations applied
- [ ] Static files loading
- [ ] Error pages working
- [ ] Default credentials changed

### Security Checklist
- [ ] HTTPS enabled
- [ ] Debug mode disabled
- [ ] Secret key generated
- [ ] Admin credentials changed
- [ ] Environment variables secure
- [ ] Security headers enabled

## 🎉 Success!

Your Claims Management System is now deployed and ready to use!

**Next Steps:**
1. Change the default admin password
2. Load your claims data using the management commands
3. Configure any additional settings
4. Set up monitoring and alerts
5. Share the application URL with your team

---

**Need Help?** Check the troubleshooting section or contact support!
