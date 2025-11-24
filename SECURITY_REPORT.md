# Security Vulnerability Assessment Report

## Summary
I have performed a security check on your project and identified a few areas for improvement, primarily related to **Cross-Site Request Forgery (CSRF)** protection and **Rate Limiting**. I have applied fixes to secure your application.

## Findings & Fixes

### 1. CSRF Protection
**Issue**: Several API endpoints (`contact_form`, `subscribe`, `chat_with_ai`) were marked with `@csrf_exempt`, bypassing Django's built-in protection against Cross-Site Request Forgery attacks.
**Fix**:
- Removed `@csrf_exempt` from all views.
- Updated the frontend (`base.html`) to correctly fetch the CSRF token from cookies and include it in the `X-CSRFToken` header for all AJAX requests.
- Added `@ensure_csrf_cookie` to the `home` view to guarantee the CSRF cookie is set when a user visits the site.

### 2. Rate Limiting
**Issue**: The contact form and AI chat endpoints had no rate limiting, making them vulnerable to spam or abuse (e.g., draining your email quota or AI API credits).
**Fix**:
- Implemented a custom `@rate_limit` decorator.
- Applied the following limits:
    - **Contact Form**: 5 requests per 5 minutes.
    - **AI Chat**: 10 requests per minute.
    - **Content Summary**: 10 requests per minute.

### 3. Code Cleanup
**Issue**: Found a duplicate `subscribe` view function in `views.py`.
**Fix**: Removed the redundant function to avoid confusion and potential bugs.

### 4. General Configuration
**Status**: **PASSED**
- `DEBUG` is correctly configured to be `False` in production (via environment variables).
- `SECRET_KEY` is loaded from environment variables.
- `ALLOWED_HOSTS` is properly configured.
- Security middleware (SSL redirect, HSTS, secure cookies) is enabled for production.
- `.env` and `db.sqlite3` are correctly ignored in `.gitignore`.

## Recommendations
- **Environment Variables**: Ensure all production environment variables (like `SECRET_KEY`, `SENDGRID_API_KEY`, `GEMINI_API_KEY`) are set securely on your hosting platform (Heroku).
- **Monitoring**: Keep an eye on your logs for any `429 Too Many Requests` errors, which would indicate the rate limits are being hit (either by attackers or legitimate heavy usage).
