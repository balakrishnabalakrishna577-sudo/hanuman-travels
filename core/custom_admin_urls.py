from django.urls import path
from . import custom_admin_views as v

urlpatterns = [
    path('login/', v.admin_login, name='admin_login'),
    path('logout/', v.admin_logout, name='admin_logout'),
    path('', v.dashboard, name='custom_admin_dashboard'),

    # Bookings
    path('bookings/tours/', v.tour_bookings, name='custom_admin_tour_bookings'),
    path('bookings/tours/<int:pk>/edit/', v.tour_booking_edit, name='custom_admin_tour_booking_edit'),
    path('bookings/cars/', v.car_bookings, name='custom_admin_car_bookings'),
    path('bookings/cars/<int:pk>/edit/', v.car_booking_edit, name='custom_admin_car_booking_edit'),
    path('bookings/<str:booking_type>/<int:pk>/status/', v.booking_status, name='custom_admin_booking_status'),
    path('bookings/tours/<int:pk>/payment-status/', v.booking_payment_status, name='custom_admin_payment_status'),

    # Content — Tours
    path('tours/', v.tours_list, name='custom_admin_tours'),
    path('tours/add/', v.tour_add, name='custom_admin_tour_add'),
    path('tours/<int:pk>/edit/', v.tour_edit, name='custom_admin_tour_edit'),
    path('tours/<int:pk>/delete/', v.tour_delete, name='custom_admin_tour_delete'),

    # Content — Destinations
    path('destinations/', v.destinations_list, name='custom_admin_destinations'),
    path('destinations/add/', v.destination_add, name='custom_admin_destination_add'),
    path('destinations/<int:pk>/edit/', v.destination_edit, name='custom_admin_destination_edit'),
    path('destinations/<int:pk>/delete/', v.destination_delete, name='custom_admin_destination_delete'),

    # Content — Vehicles
    path('vehicles/', v.vehicles_list, name='custom_admin_vehicles'),
    path('vehicles/add/', v.vehicle_add, name='custom_admin_vehicle_add'),
    path('vehicles/<int:pk>/edit/', v.vehicle_edit, name='custom_admin_vehicle_edit'),
    path('vehicles/<int:pk>/delete/', v.vehicle_delete, name='custom_admin_vehicle_delete'),

    # Content — Blog
    path('blog/', v.blog_list, name='custom_admin_blog'),
    path('blog/add/', v.blog_add, name='custom_admin_blog_add'),
    path('blog/<int:pk>/edit/', v.blog_edit, name='custom_admin_blog_edit'),
    path('blog/<int:pk>/delete/', v.blog_delete, name='custom_admin_blog_delete'),

    # Content — Gallery
    path('gallery/', v.gallery_list, name='custom_admin_gallery'),
    path('gallery/add/', v.gallery_add, name='custom_admin_gallery_add'),
    path('gallery/<int:pk>/edit/', v.gallery_edit, name='custom_admin_gallery_edit'),
    path('gallery/<int:pk>/delete/', v.gallery_delete, name='custom_admin_gallery_delete'),

    # Users & CRM
    path('users/', v.users_list, name='custom_admin_users'),
    path('users/<int:pk>/edit/', v.user_edit, name='custom_admin_user_edit'),
    path('messages/', v.contact_messages, name='custom_admin_messages'),
    path('messages/<int:pk>/read/', v.mark_message_read, name='custom_admin_mark_read'),
    path('messages/<int:pk>/delete/', v.delete_message, name='custom_admin_delete_message'),
    path('newsletter/', v.newsletter_list, name='custom_admin_newsletter'),
    path('newsletter/<int:pk>/delete/', v.newsletter_delete, name='custom_admin_newsletter_delete'),
    path('testimonials/', v.testimonials_list, name='custom_admin_testimonials'),
    path('testimonials/add/', v.testimonial_add, name='custom_admin_testimonial_add'),
    path('testimonials/<int:pk>/edit/', v.testimonial_edit, name='custom_admin_testimonial_edit'),
    path('testimonials/<int:pk>/delete/', v.testimonial_delete, name='custom_admin_testimonial_delete'),
    # Reviews
    path('reviews/', v.reviews_list, name='custom_admin_reviews'),
    path('reviews/<int:pk>/approve/', v.review_approve, name='custom_admin_review_approve'),
    path('reviews/<int:pk>/delete/', v.review_delete, name='custom_admin_review_delete'),
    # Airport Transfers
    path('bookings/airport-transfers/', v.airport_transfers, name='admin_airport_transfers'),
    path('bookings/airport-transfers/<int:pk>/status/', v.airport_transfer_status, name='admin_airport_transfer_status'),
]
