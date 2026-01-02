from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Article, CaseStudy

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 
            'project_list', 
            'article_list', 
            'certification_list', 
            'case_study_list',
            'privacy_policy'
        ]

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Project.objects.all()
        
    def lastmod(self, obj):
        return obj.created_at

class ArticleSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.all()
        
    def lastmod(self, obj):
        return obj.date_posted

class CaseStudySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return CaseStudy.objects.all()
        
    def lastmod(self, obj):
        return obj.date_posted