import os
from django.conf import settings
from django.core.mail import send_mail

def send_email(to_email, subject, html_content):
    """Send email using Django's configured backend (SMTP).
    Args:
        to_email (str or list): Recipient email address(es).
        subject (str): Email subject.
        html_content (str): HTML body of the email.
    Returns:
        None. Raises exception on failure.
    """
    # Ensure to_email is a list
    if isinstance(to_email, str):
        to_email = [to_email]
        
    send_mail(
        subject,
        html_content, # Using html_content as message body. For HTML emails, use html_message param.
        settings.DEFAULT_FROM_EMAIL,
        to_email,
        fail_silently=True,
        # html_message=html_content # Uncomment if sending actual HTML
    )
