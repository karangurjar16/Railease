from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('log/', log, name="log"),
     path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('user_logout/', user_logout, name='user_logout'),
    # path('user_logout/', user_logout, name='user_logout'),
    path('book/', book, name='book'),
    path('search/',u_search, name='u_search'),
    path('get_train_number_suggestions/', get_train_number_suggestions, name='get_train_number_suggestions'),   

]