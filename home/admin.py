from django.contrib import admin
from .models import Blog, Comment

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'text')
    list_filter = ('created_on', 'author')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ('created_on',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
