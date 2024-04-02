from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.utils import timezone
import uuid
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Register
from django.contrib.auth.models import User  
from datetime import date, datetime

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
            register = Register.objects.create(user = user)
            login(request, user)
            return redirect('user_login')  # Replace 'user_login' with your actual login URL name
    else:
        form = RegistrationForm()
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return render(request,'dashboard.html')
                else:
                    return redirect('home')
            else:
                return redirect('user_register')
    else:
        form = AuthenticationForm()

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




def booking(request):
    if request.method == 'POST':
        source = request.POST.get('source', None)
        destination = request.POST.get('destination', None)
        date = request.POST.get('date', None)
        print(date)
        journey_date = datetime.strptime(date, '%Y-%m-%d')
        print(journey_date)
        city_code1 = source.split(" - ", 2)[1].lower() if ' - ' in source else source.lower() if source else None
        city_code2 = destination.split(" - ", 2)[1].lower() if ' - ' in destination else destination.lower() if destination else None
        route = city_code1 + " - " + city_code2
        if city_code1 and city_code2 and journey_date:
            if not Route.objects.filter(station=city_code1).exists() or not Route.objects.filter(station=city_code2).exists():
                return HttpResponse("Invalid source or destination provided.")

            train_routes = Route.objects.filter(Q(station=city_code1) | Q(station=city_code2)) 
            my_values = set(item.train for item in train_routes)
            train_id_to_number = {train.train_number for train in my_values}
            result = []
            for train_id in train_id_to_number:
                routes1 = Route.objects.filter(train_id=train_id, station__iexact=city_code1)
                routes2 = Route.objects.filter(train_id=train_id, station__iexact=city_code2)

                if routes1.exists() and routes2.exists():
                    route1 = routes1.first()
                    route2 = routes2.first()
                    di1 = route1.distance
                    di2 = route2.distance

                    if di2 > di1:
                            total_distance = di2 - di1
                            charge = route2.charge - route1.charge
                            result.append({
                                'train_name': route1.train.train_name,
                                'train_number': route1.train.train_number,
                                'start': route1.arrival_time,
                                'end': route2.arrival_time,
                                'charge': charge,
                                'distance': total_distance,
                            })
        fare = charge
        date = journey_date
        helper = Helper.objects.create(route=route, date=date, charge=fare)
        con = helper.id
    return render(request, 'booking.html', {'result': result, 'source': source, 'destination': destination,'con':con,'date':date})


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
    try:
        profile = Register.objects.get(user=user)
    except Register.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        about = request.POST.get('about')
        mobile = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('user_profile') 
        else:
            form = CustomPasswordChangeForm(request.user)

        if full_name:
           
            if ' ' in full_name:
                first_name, last_name = full_name.split(' ', 1)
            else:
                first_name = full_name
                last_name = ''
        else:
            first_name = ''
            last_name = ''

        if profile is None:
            # If profile doesn't exist, create a new one
            profile = Register.objects.create(
                user=user,
                mobile=mobile,
                add=address,
                about=about,
                fname=first_name,
                lname=last_name
            )
        else:
            # If profile exists, update its fields
            profile.mobile = mobile
            profile.add = address
            profile.about = about
            # Update first name and last name in the User model
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()  # Save the changes to the User model

            # Update first name and last name in the Register model
            profile.fname = first_name
            profile.lname = last_name
            profile.save()

        # Redirect to user profile page
        return redirect('user_profile')

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'user_profile.html', context)




def booknow(request, con, train_number):
    helper = Helper.objects.get(id=con)
    train = Train.objects.get(train_number=train_number)
    charge = helper.charge
    charge1 = int(charge)
    error = False
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    route = helper.route
    date = helper.date
    pro = Travel.objects.filter(user=user1)
    book = Book.objects.filter(user=user1)
    total = 0
    for i in pro:
        if i.status != "set":
            total += i.fare

    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        gender = request.POST["gender"]

        user_id = user1.user_id  
        timestamp = timezone.now().strftime("%H%M%S")
        unique_id = str(uuid.uuid4())[:4]  
        travel_id = f"T{user_id}{timestamp}{unique_id}"

        passengers = Travel.objects.create(
            user=user1,
            train=train,
            name=name,
            travel_id=travel_id,  
            gender=gender,
            age=age,
            route=route,
            date1=date,
            fare=charge
        )
        book_ticket = Book.objects.create(
            travel=passengers,
            user=user1,
            route=route,
            date2=date,
            fare=total
        )
        print(passengers)
        if passengers:
            error = True

    d = {'charge': charge, 'data2': train, 'pro': pro, 'total': total, 'book': book, 'route1': route, 'error': error, 'con': con}
    return render(request, 'booknow.html', d)



def Delete_passenger(request,pid,con,train_number):
    data = Travel.objects.get(id=pid)
    data.delete()
    messages.info(request,'Passenger Deleted Successfully')
    return redirect('booknow',con,train_number)

def card_detail(request,total,con,train_number):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    data2 = Train.objects.get(train_number=train_number)
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Travel.objects.filter(user=user1)
    book = Book.objects.filter(user=user1)
    count=0
    pro1 = 0
    if request.method == "POST":
        error=True
        for i in pro:
            count = i.name
            if i.status != "set":
                i.status="set"
                i.save()
        return redirect('my_booking')

    total1=total
    d = {'user':user1,'data2':data2,'pro':pro,'pro1':pro1,'total':total1,'book':book,'error':error,'count':count}
    return render(request,'card_detail.html',d)

def my_booking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Travel.objects.filter(user=user1)
    book = Book.objects.filter(user=user1)
    d = {'user':user1,'pro':pro,'book':book}
    return render(request,'my_booking.html',d)
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def view_ticket(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    book = get_object_or_404(Travel, id=pid)
    ticket_id = book.travel_id
    train_name = book.train.train_name
    train_number = book.train.train_number
    route = book.route
    name = book.name
    age = book.age
    gender = book.gender
    date = book.date1
    fare = book.fare

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{ticket_id}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    header_style = getSampleStyleSheet()["Title"]
    header_text = Paragraph("RAILEASE", header_style)
    elements.append(header_text)
    data = [
        ["Ticket ID:", ticket_id],
        ["Train Name & No.:", f"{train_name} ({train_number})"],
        ["Route:", route],
        ["Name:", name],
        ["Age:", age],
        ["Gender:", gender],
        ["Date:", date],
        ["Fare:", fare]
    ]

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table and apply style
    ticket_table = Table(data)
    ticket_table.setStyle(style)

    # Add table to document
    elements.append(ticket_table)

    # Build PDF document
    doc.build(elements)

    return response

from datetime import datetime, timedelta
from django.utils import timezone

from django.utils import timezone

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Register, Travel, Book

def cancelation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user2 = User.objects.filter(username=request.user.username).get()
    user1 = Register.objects.filter(user=user2).get()
    pro = Travel.objects.filter(user=user1)
    book = Book.objects.filter(user=user1)
    now = timezone.now().date()
    next_day = now + timedelta(days=1)
    d = {'user': user1, 'pro': pro, 'book': book, 'now': next_day}
    return render(request, 'cancelation.html', d)

def delete_my_booking(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=False
    pro = Travel.objects.get(id=pid)
    pro.delete()
    error=True
    d = {'error':error}
    return render(request,'cancelation.html',d)
