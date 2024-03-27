from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import Http404 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from .models import *
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def index(request):
    if request.user.is_superuser:
        logout(request) 
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('user_login')  # Replace 'index' with your actual home page URL
    else:
        form = RegistrationForm()

    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = LoginForm()

    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


def get_train(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if 'term' in request.GET:
            term = request.GET.get('term')
            qs = Train.objects.filter(train_number__icontains=term) | Train.objects.filter(train_name__icontains=term)
            suggestions = [{'label': f"{train.train_number} - {train.train_name}", 'value': train.train_number} for train in qs]
            return JsonResponse(suggestions, safe=False)
        return render(request, 'user_search.html')
    else:
        return redirect('user_login')  


def searched_train(request):
    selected_train_number_str = request.POST.get('selectedTrain', None)

    if selected_train_number_str is None:
        error_message = "No train number provided."
        return render(request, 'user_search.html', {'error_message': error_message, 'result': None})

    try:
        selected_train_number = int(selected_train_number_str)
    except (ValueError, TypeError):
        error_message = f"Invalid train number: {selected_train_number_str}"
        return render(request, 'user_search.html', {'error_message': error_message, 'result': None})

    try:
        result = Train.objects.get(train_number=selected_train_number)
        context = {'result': result}
    except Train.DoesNotExist:
        error_message = f"Train with number {selected_train_number} not found."
        return render(request, 'user_search.html', {'error_message': error_message, 'result': None})

    return render(request, 'user_search.html', context)


from django.db.models import Q
from django.http import HttpResponse

from django.db.models import Q
from django.http import HttpResponse

from datetime import datetime

def booking(request):
    if request.method == 'POST':
        source = request.POST.get('source', None)
        destination = request.POST.get('destination', None)
        journey_date = request.POST.get('date', None)  # Get the journey date
        
        # Convert journey date to datetime object
        journey_date = datetime.strptime(journey_date, '%Y-%m-%d') if journey_date else None
        
        city_code1 = source.split(" - ", 2)[1].lower() if ' - ' in source else source.lower() if source else None
        city_code2 = destination.split(" - ", 2)[1].lower() if ' - ' in destination else destination.lower() if destination else None

        if city_code1 and city_code2 and journey_date:
            # Check if city codes exist in the database
            if not Route.objects.filter(station=city_code1).exists() or not Route.objects.filter(station=city_code2).exists():
                return HttpResponse("Invalid source or destination provided.")

            train_routes = Route.objects.filter(Q(station=city_code1) | Q(station=city_code2)) 
            my_values = set(item.train for item in train_routes)
            train_id_to_number = {train.train_number for train in my_values} 
            
            result = []
            for route in sorted(train_id_to_number, key=lambda x: Route.objects.filter(train_id=x, station=city_code1).first().arrival_time):
                ro1 = Route.objects.filter(train_id=route, station=city_code1)
                ro2 = Route.objects.filter(train_id=route, station=city_code2)
                
                if ro1.exists() and ro2.exists():
                    di1 = ro1.first().distance
                    di2 = ro2.first().distance
                    
                    if di2 > di1:
                        try:
                            route1 = ro1.first()
                            route2 = ro2.first()
                            total_distance = di2 - di1
                            charge = route1.charge
                            
                            # Construct the result dictionary
                            result.append({
                                'train_name': route1.train.train_name,
                                'train_number': route1.train.train_number,
                                'start': route1.arrival_time,
                                'end': route2.arrival_time,
                                'charge': charge,
                                'distance': total_distance,
                                'journey_date': journey_date  # Add journey date to result
                            })
                        except Train.DoesNotExist:
                            print(f"Train with train_number {route} does not exist.")
        else:
            return HttpResponse("Please provide both source, destination, and journey date.")

    return render(request, 'booking.html', {'result': result, 'source': source, 'destination': destination, 'journey_date': journey_date})


def get_station(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if 'term' in request.GET:
            term = request.GET.get('term')
            qs = Station.objects.filter(station_code__icontains=term) | Station.objects.filter(station_name__icontains=term)
            suggestions = [{'label': f"{station.station_code} - {station.station_name}", 'value': station.station_code} for station in qs]
            return JsonResponse(suggestions, safe=False)
        return render(request, 'booking.html')
    else:
        return redirect('user_login')

def user_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request,'user_profile.html', context)

def booknow(request):
    # Logic to fetch train details based on train_number and date
    # Assuming train_details is a dictionary containing train information
    train_number = request.GET.get('train_number')
    date = request.GET.get('date')
    train_details = {
        'train_number': train_number,
        'train_name': 'Sample Train Name',
        'date':date,
          # Assuming date is passed as an argument to the view
        # Add other train details as needed
    }
    return render(request, 'booknow.html', {'train_details': train_details})