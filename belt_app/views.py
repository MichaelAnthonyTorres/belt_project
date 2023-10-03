from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validate(request.POST)

    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')

    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, 'You have successfully registered')

        return redirect('/dashboard')

def login(request):
    if request.method == 'POST':
        user = User.objects.authenticate(request.POST.get('email', None), request.POST.get('password', None))
        if user:
            request.session['user_id'] = user.id
            messages.success(request, 'You have successfully logged in')

            return redirect('/dashboard')

        else:
            messages.add_message(request, messages.ERROR, 'invalid credentials')
            return redirect('/')

    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    users = User.objects.get(id=request.session['user_id'])
    context ={
        'user': users,
        'trips': Trip.objects.all()
    }
    return render(request, 'dashboard.html', context)

def add_trip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    users = User.objects.get(id=request.session['user_id'])
    context = {
        'user': users
    }
    return render(request, 'add_trip.html', context)

def create(request):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user: 
        return redirect('index')

    if request.method == 'POST':
        errors = Trip.objects.validate(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect('/trips/new')

        trip = Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan = request.POST['plan'],
            traveler = user
        )

        return redirect('/dashboard')

    else:
        return render(request, 'add_trip.html')

def one_trip(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'one_trip.html', context)

def edit(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'current_user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit.html', context)

def remove(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    
    return redirect('/dashboard')

def update(request, trip_id):
    errors = Trip.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f'/trips/edit/{trip_id}')
    
    trips = Trip.objects.get(id=trip_id)
    trips.destination = request.POST['destination']
    trips.start_date = request.POST['start_date']
    trips.end_date = request.POST['end_date']
    trips.plan = request.POST['plan']
    trips.save()

    return redirect('/dashboard')


# Only functionality i could not get was for my update to actually update the html with the updated information.