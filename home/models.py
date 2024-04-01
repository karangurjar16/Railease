from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.CharField(max_length=10,null=True)
    add = models.CharField(max_length=100,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10,null=True)
    about = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.user.first_name
    
class Train(models.Model):
    train_number = models.CharField(max_length=50, primary_key = True)
    train_name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_number}"
    
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
    charge = models.IntegerField(null = True)
    arrival_time = models.TimeField()
    distance = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.train.train_number} - {self.station}"
    
class Travel(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    travel_id = models.CharField(max_length=100, null=True, unique=True)  # Make it unique
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=30, null=True)
    route = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=30, null=True)
    date1 = models.DateField(null=True)
    fare = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.train.train_number} - {self.name}"

class Book(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE, null=True)
    route = models.CharField(max_length=100, null=True)
    date2 = models.DateField(null=True)
    fare = models.IntegerField(null=True)

    def __str__(self):
        return self.user.user.username+" "+self.route


class Helper(models.Model):
    route = models.CharField(max_length=100)
    date = models.DateField()
    charge = models.IntegerField(null = True)

    def __str__(self):
        return f"{self.route} - {self.date}"