
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path
from home.views import *
from customadmin.urls import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('',include('home.urls')),
    path('admin/',include('customadmin.urls'))

]
