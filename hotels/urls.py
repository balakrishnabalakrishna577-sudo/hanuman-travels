from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('<slug:slug>/', views.hotel_detail, name='hotel_detail'),
    path('book/<slug:hotel_slug>/', views.book_hotel, name='book_hotel'),
]
