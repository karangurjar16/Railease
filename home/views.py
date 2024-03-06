from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import Http404 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Replace 'index' with your actual home page URL
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'index' with your actual home page URL
    else:
        form = LoginForm()

    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')
def log(request):
    return render(request,'log.html')
def book(request):
    if (request.user.is_authenticated):
        return render(request,'booking.html')
    else:
        return redirect('user_login')
def booking(request):
    return redirect('home')
def u_search(request):
    if (request.user.is_authenticated):
        if request.method == 'POST':
            query = request.POST.get('query')
            if query:
                searched_train = Train.objects.filter(train_number=query).first()
                if searched_train:
                    return render(request, 'searched_train.html', {'searched_train': searched_train})
                else:
                    message = "Train not found."
                    return render(request, 'user_search.html', {'query': query, 'message': message})
            else:
                message = "Please provide a train number."
                return render(request, 'user_search.html', {'message': message})
        else:
            return render(request, 'user_search.html')
    else:
        return redirect('user_login')
        
def searched_train(request, train_number):
    train = get_object_or_404(Train, train_number=train_number)
    context = {'train': train}
    return render(request, 'searched_train.html', context)
from django.http import JsonResponse

def get_train_number_suggestions(request):
    input_text = request.GET.get('input', '')
    
    # Fetch train numbers that start with the input_text
    suggestions = Train.objects.filter(train_number__startswith=input_text).values_list('train_number', flat=True)
    
    return JsonResponse({'suggestions': list(suggestions)})
    