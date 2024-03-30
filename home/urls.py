from django.urls import path

from customadmin.views import dashboard


from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('login/', user_login, name='user_login'),
    path('admin/dashboard/', dashboard,name = "dashboard"),
    path('register/', user_register, name='user_register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('get_train/',get_train,name="get_train"),
    path('search/',searched_train, name='searched_train'),
    path('book/',booking, name='booking'),
    path('get_station/',get_station,name="get_station"),
    path('user_profile/',user_profile,name="user_profile"),
    path('booknow/(?P<con>[0-9]+)/(?P<train_number>[0-9]+)/', booknow, name='booknow'),
    path('delete_passenger/(?P<pid>[0-9]+)/(?P<con>[0-9]+)/<str:train_number>/',Delete_passenger,name="delete_passenger"),
    path('card_detail/(?P<total>[0-9]+)/(?P<con>[0-9]+)/(?P<train_number>[0-9]+)/',card_detail,name="card_detail"),
    path('my_booking/',my_booking,name="my_booking"),



]