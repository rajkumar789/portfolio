from django.contrib import admin
from .models import Project, Article, Certification, Subscription
from markdownx.admin import MarkdownxModelAdmin

class ProjectAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'created_at', 'views')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

class ArticleAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'date_posted', 'read_time', 'views')
    list_filter = ('date_posted',)
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}

class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuing_organization', 'issue_date')
    list_filter = ('issue_date',)
    search_fields = ('title', 'issuing_organization')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    search_fields = ('email',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Subscription, SubscriptionAdmin)