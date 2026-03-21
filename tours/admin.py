from django.contrib import admin
from django.utils.html import format_html
from .models import TourPackage, TourImage, Itinerary, IncludedService, ExcludedService, Review


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 2
    fields = ['image', 'caption', 'is_primary']


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1
    fields = ['day', 'title', 'description', 'meals', 'accommodation']


class IncludedInline(admin.TabularInline):
    model = IncludedService
    extra = 2
    fields = ['item']


class ExcludedInline(admin.TabularInline):
    model = ExcludedService
    extra = 2
    fields = ['item']


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'destination', 'tour_type', 'duration_days',
                    'price_per_person', 'discounted_price', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active', 'tour_type', 'difficulty', 'destination']
    search_fields = ['title', 'destination__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_active']
    list_per_page = 15
    inlines = [TourImageInline, ItineraryInline, IncludedInline, ExcludedInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'destination', 'tour_type', 'difficulty', 'thumbnail')
        }),
        ('Description', {
            'fields': ('description', 'highlights')
        }),
        ('Duration & Pricing', {
            'fields': ('duration_days', 'duration_nights', 'price_per_person', 'discounted_price', 'max_group_size', 'min_age')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="45" style="object-fit:cover;border-radius:6px;" />', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Photo'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'star_rating', 'title', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['user__username', 'tour__title', 'title']
    list_editable = ['is_approved']
    actions = ['approve_reviews', 'reject_reviews']
    date_hierarchy = 'created_at'

    def star_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color:#ff8c00;">{}</span>', stars)
    star_rating.short_description = 'Rating'

    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} review(s) approved.')
    approve_reviews.short_description = '✓ Approve selected reviews'

    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} review(s) rejected.')
    reject_reviews.short_description = '✗ Reject selected reviews'
