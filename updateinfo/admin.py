from django.contrib import admin
from .models import NewsItem, Site


class NewsItemAdmin(admin.ModelAdmin):
    list_filter = 'title', 'site'
    list_display = 'title', 'site', 'url'
    search_fields = 'title', 'site'

admin.site.register(NewsItem, NewsItemAdmin)

class SiteAdmin(admin.ModelAdmin):
    list_display = 'name',

admin.site.register(Site, SiteAdmin)

