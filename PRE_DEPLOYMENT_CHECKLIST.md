# Pre-Deployment Checklist for Heroku

## ✅ Completed Items

### Configuration Files
- ✅ `Procfile` - Configured with Gunicorn
- ✅ `requirements.txt` - All dependencies listed
- ✅ `runtime.txt` - Python 3.13.1 specified
- ✅ `.env.example` - Template for environment variables
- ✅ `.gitignore` - Excludes sensitive files

### Django Settings
- ✅ Database: PostgreSQL via `DATABASE_URL`
- ✅ Static files: Whitenoise configured
- ✅ Media files: Cloudinary configured
- ✅ Environment variables: All settings from env
- ✅ `DEBUG=False` for production
- ✅ `ALLOWED_HOSTS` configured

### Models & Features
- ✅ SEO-friendly slugs for Articles and Projects
- ✅ Soft delete/trash functionality
- ✅ Email notifications (SMTP)
- ✅ Newsletter subscription
- ✅ AI chat and summarization
- ✅ Contact form

### Cleanup
- ✅ Removed test scripts
- ✅ Removed debug files
- ✅ Updated `.gitignore`

## 📋 Deployment Steps

### 1. Create Heroku App
```bash
heroku create your-portfolio-name
```

### 2. Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:essential-0
```

### 3. Set Environment Variables
```bash
# Django
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app.herokuapp.com,rajsunar.live"
heroku config:set SITE_URL="https://your-app.herokuapp.com"

# Gemini AI
heroku config:set GEMINI_API_KEY="your-key"

# Cloudinary
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud"
heroku config:set CLOUDINARY_API_KEY="your-key"
heroku config:set CLOUDINARY_API_SECRET="your-secret"

# Email (SMTP)
heroku config:set EMAIL_HOST="mail.privateemail.com"
heroku config:set EMAIL_PORT="587"
heroku config:set EMAIL_USE_TLS="True"
heroku config:set EMAIL_HOST_USER="rajsunar@rajsunar.live"
heroku config:set EMAIL_HOST_PASSWORD="your-password"
heroku config:set DEFAULT_FROM_EMAIL="rajsunar@rajsunar.live"
```

### 4. Deploy
```bash
git add .
git commit -m "Ready for production deployment"
git push heroku main
```

### 5. Run Migrations
```bash
heroku run python manage.py migrate
```

### 6. Create Superuser
```bash
heroku run python manage.py createsuperuser
```

### 7. Test Deployment
- Visit: `https://your-app.herokuapp.com`
- Admin: `https://your-app.herokuapp.com/admin/`
- Test features:
  - ✅ Articles and Projects display
  - ✅ Contact form sends email
  - ✅ Newsletter subscription works
  - ✅ AI chat/summarization works
  - ✅ Images load from Cloudinary

## 🔧 Post-Deployment

### Update Domain (Optional)
```bash
heroku domains:add rajsunar.live
heroku domains:add www.rajsunar.live
```

Update DNS:
- CNAME: `www` → `your-app.herokuapp.com`
- ALIAS/ANAME: `@` → `your-app.herokuapp.com`

### Monitoring
```bash
# View logs
heroku logs --tail

# Check dyno status
heroku ps

# Restart if needed
heroku restart
```

## 🚨 Important Notes

1. **Database**: SQLite → PostgreSQL (migration automatic)
2. **Static Files**: Served by Whitenoise
3. **Media Files**: Stored in Cloudinary (not on Heroku filesystem)
4. **Environment**: All sensitive data in environment variables
5. **Debug Mode**: OFF in production (`DEBUG=False`)

## ✨ Your Portfolio is Production-Ready!

All test files removed, configurations verified, and ready to deploy!
