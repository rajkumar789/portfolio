import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from portfolio.models import Project, Article, Certification

print(f"Projects count: {Project.objects.count()}")
print(f"Articles count: {Article.objects.count()}")
print(f"Certifications count: {Certification.objects.count()}")
