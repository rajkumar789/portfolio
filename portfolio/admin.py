from django.contrib import admin
from .models import Project, ProjectImage, Article, Certification, Subscription, CaseStudy, CaseStudyImage


class ProjectImageInline(admin.TabularInline):
    from .models import ProjectImage
    model = ProjectImage
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'views', 'likes')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'read_time', 'views', 'likes')
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

class CaseStudyImageInline(admin.TabularInline):
    model = CaseStudyImage
    extra = 1

class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'views', 'likes')
    inlines = [CaseStudyImageInline]
    list_filter = ('date_posted',)
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)