import os
import django
import cloudinary
import cloudinary.api

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

try:
    config = cloudinary.config()
    print(f"Testing Cloudinary with API Key: {config.api_key}")
    # Ping Cloudinary to check credentials
    result = cloudinary.api.ping()
    print("Success! Cloudinary API connection established.")
    print(f"Response: {result}")
except Exception as e:
    print(f"Error: {e}")
