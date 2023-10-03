from django.urls import path
from . import views

urlpatterns = [
    # Login Paths
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    # dashboard paths 
    path('dashboard', views.dashboard),
    path('trips/new', views.add_trip),
    path('trips/<int:trip_id>', views.one_trip),
    path('trips/edit/<int:trip_id>', views.edit),
    # editing paths
    path('create', views.create),
    path('remove/<int:trip_id>', views.remove),
    path('update/<int:trip_id>', views.update)
]