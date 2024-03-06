
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('',include('home.urls')),
    path('admin/',include('customadmin.urls'))

]
