from django.urls import path
from . import views

app_name = 'ritual'

urlpatterns = [
    path('', views.ritual_home, name='home'),
]
