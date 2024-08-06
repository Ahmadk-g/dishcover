from django.urls import path
from . import views


urlpatterns = [
    path('', views.Recipes.as_view(), name='recipes'),
    path('addrecipe/', views.AddRecipe.as_view(), name='add_recipes'),
    
]