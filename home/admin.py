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