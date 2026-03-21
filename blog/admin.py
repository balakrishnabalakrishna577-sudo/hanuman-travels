from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'author', 'category',
                    'is_published', 'views', 'created_at']
    list_filter = ['is_published', 'category', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_published']
    list_per_page = 15
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'author', 'category', 'thumbnail')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'tags')
        }),
        ('Publishing', {
            'fields': ('is_published', 'views', 'created_at', 'updated_at')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="45" style="object-fit:cover;border-radius:6px;" />', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Cover'
