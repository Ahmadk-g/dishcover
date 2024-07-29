from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecipeList.as_view(), name='Recipes'),
]