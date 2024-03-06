from django.contrib import admin
from django.urls import include, path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',admin_login, name = "admin_login"),
    path('dashboard/', dashboard,name = "dashboard"),
    path('view_train/',view_train,name = "view_train"),
    path('add_train/',add_train,name = "add_train"),
    path('search/', search_train, name='search_train'),
    path('update/<str:train_number>/', update_train, name='update_train'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    path('delete_train/<int:train_number>/', delete_train, name='delete_train'),
    path('search_station/', search_station, name='search_station'),
    path('view_station/',view_station,name="view_station"),
    path('add_station/',add_station,name = "add_station"),
    path('update_station/<str:station_code>/', update_station, name='update_station'),
    path('delete_station/<str:station_code>/', delete_station, name='delete_station'),

]