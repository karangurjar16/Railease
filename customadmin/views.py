from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from home.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import Http404 
from django.contrib.auth.decorators import login_required


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard/')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            
            if not user_obj.exists():
                messages.error(request, 'Account not found. Please check your username.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username, password=password)
            
            if not user_obj:
                messages.error(request, 'Incorrect password. Please try again.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard/')
            
            return redirect('/')
        
        # Add this line to handle the case when not authenticated and not a 'POST' request
        return render(request, 'login1.html')
    
    except Exception as e:
        print(e)



def dashboard(request):
    if request.user.is_superuser:
        objs = Train.objects.all()
        x = len(objs)
        stat = Station.objects.all()
        y = len(stat)
        use = User.objects.filter(is_superuser=False)
        z = len(use)
        return render(request, 'dashboard.html', {'x': x,'y':y,'z':z})
    else:
        logout(request)
        return redirect('admin_login') 

def view_train(request):
    if (request.user.is_authenticated):
        objs = Train.objects.all()
        return render(request,'view_train.html',{'objs':objs})
    else:
        return redirect('admin_login')
    

def add_train(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)  # Assuming you have a form to handle train input
        if form.is_valid():
            form.save()
            return redirect('view_train')  # Redirect to the view train page after successful addition
    else:
        form = TrainForm()  # Assuming you have a form to handle train input

    return render(request, 'add_train.html', {'form': form})


def search_train(request):
    query = request.POST.get('query', '')
    
    if query:
        results = Train.objects.filter(train_number__icontains=query)
    else:
        results = Train.objects.all()

    return render(request, 'search_train.html', {'results': results, 'query': query})

def update_train(request, train_number):
    train = Train.objects.get(train_number=train_number)

    if request.method == 'POST':
        form = TrainUpdateForm(request.POST, instance=train)
        if form.is_valid():
            form.save()
            return render(request, 'train_updated.html', {'train_number': train_number})
    else:
        form = TrainUpdateForm(instance=train)

    return render(request, 'update_train.html', {'form': form, 'train': train, 'train_number': train_number})

def delete_train(request, train_number):
    try:
        train = Train.objects.get(train_number=train_number)
        if request.method == 'POST':
            train.delete()
            return redirect('search_train')
        return render(request, 'delete_train.html', {'train': train})
    except Train.DoesNotExist:
        return redirect('search_train')



def view_station(request):
    objs = Station.objects.all()
    return render(request,'view_station.html',{'objs':objs})

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)  # Assuming you have a form to handle train input
        if form.is_valid():
            form.save()
            return redirect('view_station')  # Redirect to the view train page after successful addition
    else:
        form = StationForm()  # Assuming you have a form to handle train input

    return render(request, 'add_station.html', {'form': form})

def update_station(request,station_code):
    station = Station.objects.get(station_code=station_code)

    if request.method == 'POST':
        form = StationUpdateForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return render(request, 'station_updated.html', {'station_code': station_code})
    else:
        form = StationUpdateForm(instance=station)

    return render(request, 'update_station.html', {'form': form, 'station': station, 'station_code': station_code})

def search_station(request):
    query = request.POST.get('query', '')
    
    if query:
        results = Station.objects.filter(station_code__icontains=query)
    else:
        results = Station.objects.all()

    return render(request, 'search_station.html', {'results': results, 'query': query})



def delete_station(request, station_code):
    try:
        station = Station.objects.get(station_code=station_code)
        if request.method == 'POST':
            station.delete()
            messages.success(request, 'Station deleted successfully.')
            return redirect('search_station')
        return render(request, 'delete_station.html', {'station': station})
    except Station.DoesNotExist:
        messages.error(request, 'Station not found.')
        return redirect('search_station')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')