from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
    path('airport-transfer/', views.airport_transfer, name='airport_transfer'),
    path('airport-transfer/success/<str:booking_id>/', views.airport_transfer_success, name='airport_transfer_success'),
]
