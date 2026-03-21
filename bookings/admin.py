from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, TravelerDetail


class TravelerInline(admin.TabularInline):
    model = TravelerDetail
    extra = 0
    fields = ['name', 'age', 'id_type', 'id_number']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'tour', 'travel_date', 'num_adults',
                    'num_children', 'total_amount_display', 'status_badge', 'payment_badge', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'user__email', 'tour__title']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    inlines = [TravelerInline]
    date_hierarchy = 'created_at'
    list_per_page = 20
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_id', 'user', 'tour', 'travel_date')
        }),
        ('Travelers', {
            'fields': ('num_adults', 'num_children', 'special_requests')
        }),
        ('Payment', {
            'fields': ('total_amount', 'status', 'payment_status', 'payment_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total_amount_display(self, obj):
        return format_html('<strong>₹{}</strong>', f'{obj.total_amount:,.0f}')
    total_amount_display.short_description = 'Amount'

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#17a2b8',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_badge(self, obj):
        colors = {
            'unpaid': '#dc3545',
            'partial': '#ffc107',
            'paid': '#28a745',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.payment_status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:0.78rem;font-weight:600;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_badge.short_description = 'Payment'
