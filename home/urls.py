from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name="home"),
     path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('get_train/',get_train,name="get_train"),
    path('search/',searched_train, name='searched_train'),
    path('book/',booking, name='booking'),
    path('get_station/',get_station,name="get_station"),



]