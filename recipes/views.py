from django.shortcuts import render
from django.views import generic
from .models import Recipe

# Create your views here.
class RecipeList(generic.TemplateView):
    queryset = Recipe.objects.filter(status=1)
    template_name = "recipes/recipes.html"