# Heroku Deployment Guide

This guide will help you deploy your Django portfolio to Heroku.

## Prerequisites

1. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
2. Git repository initialized
3. Heroku account created

## Step 1: Verify Configuration Files

Your project already has these files configured:

- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `requirements.txt` - Lists all Python dependencies
- ✅ `runtime.txt` - Specifies Python version (3.13.1)

## Step 2: Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Or let Heroku generate a name
heroku create
```

## Step 3: Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

## Step 4: Set Environment Variables

Set all required environment variables on Heroku:

```bash
# Django Settings
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com,rajsunar.live"
heroku config:set SITE_URL="https://your-app-name.herokuapp.com"

# Google Gemini AI
heroku config:set GEMINI_API_KEY="your-gemini-api-key"

# Cloudinary (Image Storage)
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud-name"
heroku config:set CLOUDINARY_API_KEY="your-api-key"
heroku config:set CLOUDINARY_API_SECRET="your-api-secret"

# Email (SMTP)
heroku config:set EMAIL_HOST="mail.privateemail.com"
heroku config:set EMAIL_PORT="587"
heroku config:set EMAIL_USE_TLS="True"
heroku config:set EMAIL_HOST_USER="rajsunar@rajsunar.live"
heroku config:set EMAIL_HOST_PASSWORD="your-email-password"
heroku config:set DEFAULT_FROM_EMAIL="rajsunar@rajsunar.live"
```

## Step 5: Deploy to Heroku

```bash
# Add Heroku remote (if not automatically added)
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

## Step 6: Run Migrations

```bash
heroku run python manage.py migrate
```

## Step 7: Create Superuser

```bash
heroku run python manage.py createsuperuser
```

## Step 8: Collect Static Files

Static files are automatically collected during deployment via the Procfile.

## Step 9: Configure Custom Domain (Optional)

If you want to use `rajsunar.live`:

```bash
heroku domains:add rajsunar.live
heroku domains:add www.rajsunar.live
```

Then update your DNS settings:
- Add CNAME record: `www` → `your-app-name.herokuapp.com`
- Add ALIAS/ANAME record: `@` → `your-app-name.herokuapp.com`

Update ALLOWED_HOSTS:
```bash
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com,rajsunar.live,www.rajsunar.live"
```

## Troubleshooting

### View Logs
```bash
heroku logs --tail
```

### Check Config Vars
```bash
heroku config
```

### Restart App
```bash
heroku restart
```

### Open App
```bash
heroku open
```

## Post-Deployment Checklist

- [ ] Visit `/admin/` and login with superuser
- [ ] Add some projects, articles, and certifications via admin
- [ ] Test contact form
- [ ] Test newsletter subscription
- [ ] Verify all images load correctly (Cloudinary)
- [ ] Test AI chat assistant
- [ ] Submit sitemap to Google Search Console
- [ ] Set up monitoring/alerts in Heroku dashboard

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `app.herokuapp.com,rajsunar.live` |
| `DATABASE_URL` | PostgreSQL connection (auto-set by Heroku) | Auto-configured |
| `SITE_URL` | Full site URL for emails | `https://rajsunar.live` |
| `GEMINI_API_KEY` | Google Gemini API key | From Google AI Studio |
| `CLOUDINARY_*` | Cloudinary credentials | From Cloudinary dashboard |
| `EMAIL_*` | SMTP credentials | From your email provider |

## Continuous Deployment

To enable automatic deployments from GitHub:

1. Go to Heroku Dashboard → Your App → Deploy tab
2. Connect your GitHub repository
3. Enable "Automatic Deploys" from main branch

Every push to main will automatically deploy!
