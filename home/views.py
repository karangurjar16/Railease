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
        return render(request, 'searched_train.html', {'error_message': error_message, 'result': None})

    try:
        selected_train_number = int(selected_train_number_str)
    except (ValueError, TypeError):
        error_message = f"Invalid train number: {selected_train_number_str}"
        return render(request, 'searched_train.html', {'error_message': error_message, 'result': None})

    try:
        result = Train.objects.get(train_number=selected_train_number)
        context = {'result': result}
    except Train.DoesNotExist:
        error_message = f"Train with number {selected_train_number} not found."
        return render(request, 'searched_train.html', {'error_message': error_message, 'result': None})

    return render(request, 'searched_train.html', context)