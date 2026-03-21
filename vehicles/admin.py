from django.contrib import admin
from django.utils.html import format_html
from .models import Vehicle, CarBooking


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'name', 'vehicle_type', 'capacity',
                    'price_per_day', 'is_ac', 'driver_included', 'is_available']
    list_filter = ['vehicle_type', 'is_available', 'is_ac', 'driver_included']
    search_fields = ['name', 'model']
    list_editable = ['is_available']
    list_per_page = 15

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="45" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Photo'


@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'vehicle', 'pickup_location',
                    'pickup_date', 'return_date', 'total_amount_display', 'status_badge']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'vehicle__name']
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
