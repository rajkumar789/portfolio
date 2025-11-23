from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .sitemaps import StaticViewSitemap

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('certifications/', views.certification_list, name='certification_list'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('search/', views.search, name='search'),
    
    # New Chat Endpoint
    path('api/subscribe/', views.subscribe, name='subscribe'),
    path('api/contact/', views.contact_form, name='contact_form'),
    path('api/chat/', views.chat_with_ai, name='chat_with_ai'),
    path('api/summarize/', views.summarize_content, name='summarize_content'),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
]
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    # The strings in this list must match the 'name' arguments in your portfolio/urls.py
    def items(self):
        return [
            'home', 
            'project_list', 
            'article_list', 
            'certification_list', 
            'privacy_policy'
        ]

    def location(self, item):
        return reverse(item)