from django import template
from django.template.defaultfilters import stringfilter
import markdown as md
import bleach
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
@stringfilter
def markdownify(value):
    # Convert markdown to HTML
    html_content = md.markdown(value, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.extra',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
    ])
    
    # Define allowed tags and attributes
    allowed_tags = [
        'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
        'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'em', 'strong', 
        'b', 'i', 'a', 'img', 'br', 'hr', 'table', 'thead', 'tbody', 
        'tr', 'th', 'td', 'style', 'dl', 'dt', 'dd', 'abbr', 'sup', 'sub'
    ]
    
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title', 'class'],
        '*': ['class', 'id'],
    }
    
    # Sanitize the HTML
    cleaned_content = bleach.clean(
        html_content, 
        tags=allowed_tags, 
        attributes=allowed_attributes, 
        strip=True
    )
    
    return mark_safe(cleaned_content)
