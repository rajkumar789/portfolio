from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField
import math

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = CKEditor5Field('Description', config_name='extends')
    technologies = models.CharField(max_length=200, help_text="Comma separated, e.g. Django, React")
    image = CloudinaryField('image', folder='projects', blank=True, null=True) 
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    full_content = CKEditor5Field('Content', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='projects')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title}"

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = CKEditor5Field('Summary', config_name='default')
    content = CKEditor5Field('Content', config_name='extends')  # Supports Markdown
    feature_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    read_time = models.CharField(max_length=50, blank=True) # e.g., "5 min read"
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Generate slug if not exists
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        # Calculate read time based on word count (approx 200 words per minute)
        word_count = len(str(self.content).split())
        minutes = math.ceil(word_count / 200)
        self.read_time = f"{minutes} min read"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    description = CKEditor5Field('Description', config_name='default', blank=True)

    image = CloudinaryField('image', folder='certifications', blank=True, null=True)
    
    class Meta:
        ordering = ['-issue_date']

    @property
    def issuer(self):
        return self.issuing_organization

    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"

# Signals to notify subscribers on new Blog or Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@receiver(post_save, sender=Article)
def send_new_article_notification(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscription.objects.all()
        if subscribers.exists():
            subject = f"New Article: {instance.title}"
            message = f"""
            Hi there!

            I've just published a new article: "{instance.title}"

            Read it here: {settings.SITE_URL}/article/{instance.id}/

            Best regards,
            Raj Kumar Sunar
            """
            recipient_list = [s.email for s in subscribers]
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

@receiver(post_save, sender=Project)
def notify_subscribers_new_project(sender, instance, created, **kwargs):
    if created:
        subject = f"New Project: {instance.title}"
        link = reverse('project_detail', args=[instance.pk])
        message = f"A new project has been added: {instance.title}\n\nCheck it out: {settings.SITE_URL}{link}\n"
        recipients = list(Subscription.objects.values_list('email', flat=True))
        if recipients:
            from .utils.email import send_email
            send_email(recipients, subject, message)

@receiver(post_save, sender=Certification)
def notify_subscribers_new_certification(sender, instance, created, **kwargs):
    if created:
        subject = f"New Certification: {instance.title}"
        # Assuming certifications are listed on the home page or a specific list page
        link = reverse('certification_list') 
        message = f"I've earned a new certification: {instance.title} from {instance.issuer}\n\nCheck it out: {settings.SITE_URL}{link}\n"
        recipients = list(Subscription.objects.values_list('email', flat=True))
        if recipients:
            from .utils.email import send_email
            send_email(recipients, subject, message)

class CaseStudy(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    summary = CKEditor5Field('Summary', config_name='default')
    content = CKEditor5Field('Content', config_name='extends')
    image = CloudinaryField('image', folder='case_studies', blank=True, null=True)
    technologies = models.CharField(max_length=200, blank=True, help_text="Comma separated, e.g. Python, SQL", default="")
    date_posted = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('case_study_detail', kwargs={'slug': self.slug})

class CaseStudyImage(models.Model):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='case_studies_gallery')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.case_study.title}"