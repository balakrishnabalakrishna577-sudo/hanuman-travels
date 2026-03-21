from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('<slug:slug>/', views.tour_detail, name='tour_detail'),
]
