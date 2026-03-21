from django.contrib import admin
from django.utils.html import format_html
from .models import Hotel, RoomType, HotelBooking


class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    fields = ['name', 'capacity', 'price_per_night', 'is_available']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'destination', 'star_display', 'phone', 'is_active']
    list_filter = ['stars', 'is_active', 'destination']
    search_fields = ['name', 'destination__name', 'address']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    list_per_page = 15
    inlines = [RoomTypeInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="45" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Photo'

    def star_display(self, obj):
        return format_html('<span style="color:#ff8c00;font-size:1rem;">{}</span>', '★' * obj.stars)
    star_display.short_description = 'Stars'


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'hotel', 'room_type', 'check_in',
                    'check_out', 'num_rooms', 'total_amount_display', 'status_badge']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'hotel__name']
    readonly_fields = ['booking_id', 'created_at']
    date_hierarchy = 'created_at'
    list_per_page = 20

    def total_amount_display(self, obj):
        return format_html('<strong>₹{}</strong>', f'{obj.total_amount:,.0f}')
    total_amount_display.short_description = 'Amount'

    def status_badge(self, obj):
        colors = {'pending': '#ffc107', 'confirmed': '#28a745', 'cancelled': '#dc3545', 'completed': '#17a2b8'}
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
