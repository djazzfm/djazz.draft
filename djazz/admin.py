from django.contrib import admin
from djazz.models import Config


class AdminConfig(admin.ModelAdmin):
    list_display = ('section', 'key', 'value')
    list_filter = ('section',)
    search_fields = ['key', 'value']
    ordering = ('section', 'key',)

admin.site.register(Config, AdminConfig)
