from django import forms
from home.models import *
from django.shortcuts import redirect, render

class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['train_number', 'train_name', 'origin', 'destination', 'departure_time', 'arrival_time','capacity']
# def train_deleted(request, train_number):
#     deleted = request.GET.get('deleted', False)
#     return render(request, 'train_deleted.html', {'deleted': deleted})

class TrainUpdateForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['train_number', 'train_name', 'origin', 'destination', 'arrival_time', 'departure_time', 'capacity']

class StationForm(forms.ModelForm):
    class Meta:
        model= Station
        fields =['station_code','station_name','city','state']
    

class StationUpdateForm(forms.ModelForm):
    class Meta:
        model = Station
        fields =['station_code','station_name','city','state']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields =['train','station','charge','arrival_time','distance']