# Portfolio Website - Raj Kumar Sunar

A modern, responsive portfolio website built with Django, featuring a clean design, AI-powered chat assistant, and dynamic content management.

## 🌟 Features

- **Modern UI/UX**: Clean, responsive design with dark mode support
- **AI Chat Assistant**: Powered by Google Gemini AI for interactive conversations
- **AI Content Summarization**: Generate quick summaries of blog posts and projects
- **Dynamic Content Management**: Django admin panel with Markdown editor
- **SEO Optimized**: Meta tags, sitemaps, and semantic HTML
- **Project Showcase**: Display projects with live demos and GitHub links
- **Blog Platform**: Share articles with syntax-highlighted code snippets
- **Certifications**: Showcase professional certifications
- **Contact Section**: Easy way for visitors to get in touch

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Integration**: Google Generative AI (Gemini)
- **Markdown**: django-markdownx for rich content editing
- **Code Highlighting**: highlight.js
- **Icons**: Lucide Icons

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/myportfolio.git
   cd myportfolio
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   GEMINI_API_KEY=your-gemini-api-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://localhost:8000` to view the site.

## 📝 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 📁 Project Structure

```
myportfolio/
├── myportfolio/          # Project settings
│   ├── settings.py       # Main settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI config
├── portfolio/           # Main app
│   ├── models.py        # Data models
│   ├── views.py         # Views
│   ├── urls.py          # App URLs
│   ├── admin.py         # Admin configuration
│   ├── templates/       # HTML templates
│   └── templatetags/    # Custom template tags
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎨 Customization

### Adding Content

1. Access the admin panel at `/admin`
2. Log in with your superuser credentials
3. Add/edit Projects, Blogs, and Certifications

### Modifying Design

- Templates are in `portfolio/templates/portfolio/`
- Static files (CSS, JS) are in `static/`
- Tailwind CSS classes are used throughout

## 🚢 Deployment

### Preparing for Production

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set up a proper web server (Gunicorn + Nginx)
5. Configure HTTPS
6. Set up static file serving

### Recommended Platforms

- **Heroku**: Easy deployment with Git
- **DigitalOcean**: App Platform or Droplets
- **AWS**: Elastic Beanstalk or EC2
- **Railway**: Simple deployment
- **Render**: Free tier available

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Raj Kumar Sunar**
- Location: West Sussex, United Kingdom
- Phone: +44 7949 514215
- Portfolio: [rajsunar.live](https://rajsunar.live)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Show your support

Give a ⭐️ if you like this project!
