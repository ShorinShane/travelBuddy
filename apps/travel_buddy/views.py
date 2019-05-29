
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 
import bcrypt

def index(request):
    return render(request, 'index.html')

def createUser(request):
    errors = User.objects.regValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(username=request.POST['username'], name=request.POST['name'], password=password_hash.decode())
        request.session['id'] = user.id 
        return redirect("/displayTravel")

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/")
    else:
        users = User.objects.filter(username=request.POST['user_name'])
        request.session['id'] = users[0].id
    return redirect("/displayTravel")


def displayTravel(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        travels = Travel.objects.all()
        joins = Join.objects.filter(user_id=request.session['id'])
        notComing = []
        Coming = []

        for join in joins:
            Coming.append(join.travel_id)
        print(Coming)
        for travel in travels:
            if travel.id not in Coming:
                notComing.append(travel)
        print(notComing)
        
        context = {
            "user": user,
            "travel": travel,
            "joins": joins,
            "notComing": notComing
        }
        return render(request, 'displayTravel.html', context)
    else:
        return redirect("/")

def createTravel(request):
    errors = Travel.objects.travelValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.add_message(request, messages.ERROR, value, key)
        return redirect("/newTravel")
    else:
        travel = Travel.objects.create(destination=request.POST['destination'], 
        description=request.POST['description'], added_by_id=request.session['id'],
        travelstart=request.POST['travelstart'],travelend=request.POST['travelend'])
        Join.objects.create(travel=travel, user_id=request.session['id'])
        return redirect("/displayTravel")
    
def newTravel(request):
    return render(request, 'newTravel.html')

def leaveTrip(request, travel_id):
    Join.objects.get(travel_id=travel_id, user_id=request.session['id']).delete()
    return redirect('/displayTravel')
    
def joinTrip(request,travel_id):
    Join.objects.create(travel_id=travel_id, user_id=request.session['id'])
    return redirect("/displayTravel")

def showTravel(request, travel_id):
    context = {
        "travel": Travel.objects.get(id=travel_id),
        "users_coming_on_trip": Join.objects.filter(travel_id=travel_id)
    }
    return render(request, 'showTravel.html', context)

def deleteTravel(request, travel_id):
    Travel.objects.get(id=travel_id).delete()
    return redirect('/displayTravel')

def logout(request):
    request.session.clear()
    print("Logged Out")
    return redirect("/")