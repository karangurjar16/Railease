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

# Create your views here.
def index(request):
    return render(request,'index.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('user_login')  # Replace 'index' with your actual home page URL
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
def book(request):
    return redirect('home')
        

    