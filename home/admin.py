from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'train_name', 'origin', 'destination', 'departure_time', 'arrival_time', 'capacity')
    search_fields = ('train_number', 'train_name', 'origin', 'destination')

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_code', 'station_name', 'city', 'state')
    search_fields = ('station_code', 'station_name', 'city', 'state')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('train', 'station', 'charge', 'arrival_time', 'distance')
    list_filter = ('train', 'station')

admin.site.register(Register)
@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    list_display = ('user', 'train', 'name', 'age', 'gender', 'route', 'status', 'date1', 'fare')
    search_fields = ('user__user.username', 'name', 'route')
    list_filter = ('status', 'date1')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'date2', 'fare')
    list_filter = ('user', 'date2')
    search_fields = ('user__username', 'route')
    
@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    list_display = ('route', 'date', 'charge')