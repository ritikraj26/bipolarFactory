from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import FlightSearchForm, SignupForm, LoginForm
from . models import Flight, Booking


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('search')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})    


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('search')
    else:
        form = SignupForm()
    return render(request, 'home/signup.html', {'form': form})



@login_required
def book_ticket(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        num_seats = int(request.POST['number_of_seats'])
        if flight.available_seats >= num_seats:
            booking = Booking(flight=flight, user=request.user, number_of_seats=num_seats)
            print(booking)
            booking.save()
            flight.available_seats -= num_seats
            flight.save()
            messages.success(request, "Booking successful!")
            return redirect('my_bookings')
        else:
            messages.error(request, "Not enough seats available.")
    return render(request, 'flights/book_ticket.html', {'flight': flight})


def search_flights(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            # Get search criteria from form.cleaned_data
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            departure_date = form.cleaned_data['departure_date']

            results = Flight.objects.filter(
                origin=origin, 
                destination=destination, 
                departure_datetime__date=departure_date  
            )
            return render(request, 'flights/search_results.html', {'results': results})
    else:
        form = FlightSearchForm()
    return render(request, 'flights/search.html', {'form': form})



@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'flights/my_bookings.html', {'bookings': bookings})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')