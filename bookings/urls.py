from django.urls import path
from . import views

urlpatterns = [
    path('book/<slug:tour_slug>/', views.create_booking, name='create_booking'),
    path('detail/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('print/<str:booking_id>/', views.booking_print, name='booking_print'),
    path('cancel/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
