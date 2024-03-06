from django.db import models

from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Train(models.Model):
    train_number = models.CharField(max_length=50,primary_key = True)
    train_name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_number} - {self.train_name}"
    
class Station(models.Model):
    station_code = models.CharField(max_length=10, unique=True)
    station_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.station_code} - {self.station_name}, {self.city}, {self.state}"

class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.CharField(max_length=100)
    charge = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    arrival_time = models.TimeField()
    distance = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.train.train_number} - {self.station}"
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train_number = models.CharField(max_length=20)
    departure_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    booking_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.train_number} - {self.departure_station} to {self.arrival_station}"

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Seat: {self.seat_number}"