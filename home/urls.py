from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name="home"),
     path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('get_train/',get_train),
    path('search/',u_search, name='u_search'),

]