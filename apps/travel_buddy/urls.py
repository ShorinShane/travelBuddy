from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('deleteTravel/<travel_id>', views.deleteTravel),
    path('showTravel/<travel_id>', views.showTravel),
    path('jointrip/<travel_id>', views.joinTrip),
    path('leavetrip/<travel_id>', views.leaveTrip),
    path('createTravel', views.createTravel),
    path('newTravel', views.newTravel),
    path('logout', views.logout),
    path('displayTravel', views.displayTravel),
    path('users/create', views.createUser),    
    path('login', views.login)
]