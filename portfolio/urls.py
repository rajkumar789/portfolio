from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProjectSitemap, ArticleSitemap, CaseStudySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'articles': ArticleSitemap,
    'case_studies': CaseStudySitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('certifications/', views.certification_list, name='certification_list'),
    path('case-studies/', views.case_study_list, name='case_study_list'),
    path('case-study/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('search/', views.search, name='search'),
    
    # New Chat Endpoint
    path('api/subscribe/', views.subscribe, name='subscribe'),
    path('api/contact/', views.contact_form, name='contact_form'),
    path('api/chat/', views.chat_with_ai, name='chat_with_ai'),
    path('api/summarize/', views.summarize_content, name='summarize_content'),
    path('api/like/', views.like_content, name='like_content'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]