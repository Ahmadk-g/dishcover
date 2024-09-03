from django.urls import path
from . import views


# Define the URL patterns for the 'about' app

urlpatterns = [
    path('', views.about_me, name='about'),
]