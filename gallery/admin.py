from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    list_per_page = 20
    date_hierarchy = 'created_at'
