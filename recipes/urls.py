from django.urls import path
from . import views


urlpatterns = [
    path('', views.Recipes.as_view(), name='recipes'),
    path('addrecipe/', views.AddRecipe.as_view(), name='add_recipes'),
    path('<slug:slug>/', views.RecipeDetails, name="recipe_details"),
    path('delete/<slug:slug>/', views.DeleteRecipe.as_view(), name="delete_recipe"),
    path('edit/<slug:slug>/', views.EditRecipe.as_view(), name="edit_recipe"),
]