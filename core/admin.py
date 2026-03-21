from django.contrib import admin
from django.utils.html import format_html
from .models import Destination, ContactMessage, Newsletter, TeamMember, Testimonial


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'state', 'is_popular', 'preview_image']
    list_filter = ['is_popular', 'country']
    search_fields = ['name', 'country', 'state']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_popular']
    list_per_page = 20

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '—'
    preview_image.short_description = 'Image'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    list_per_page = 25
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active']
    search_fields = ['email']
    list_editable = ['is_active']
    list_per_page = 30
    date_hierarchy = 'subscribed_at'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'order', 'preview_image']
    ordering = ['order']
    list_editable = ['order']

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="45" height="45" style="object-fit:cover;border-radius:50%;" />', obj.image.url)
        return '—'
    preview_image.short_description = 'Photo'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'star_rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating']
    list_editable = ['is_active']
    list_per_page = 20

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#ff8c00;font-size:1rem;">{}</span>', stars)
    star_rating.short_description = 'Rating'
