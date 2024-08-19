from django.contrib.auth.decorators import login_required
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # The Add recipe view can only be accessed if the user logged in
from django.db.models import Q # a rapper for sequel queries that allows us to write complex database operations with less code
from .models import Recipe
from .forms import RecipeForm

# Create your views here.

class AddRecipe(LoginRequiredMixin, generic.CreateView):
    """ Add recipe view """
    template_name = 'recipes/add_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddRecipe, self).form_valid(form)
    
    
class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView): 
    model = Recipe
    template_name = 'recipes/edit_recipe.html'
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):# For checking if the user is authorized to edit the post
        return self.request.user == self.get_object().author
    

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView): # order of Arg matters 
    model = Recipe
    success_url = '/recipes/'
    #template name not required, expects the template in a certain format, ("lowercase model name"_confirm_delete)
    
    def test_func(self):# For checking if the user is authorized to delete the post
        return self.request.user == self.get_object().author



class Recipes(generic.ListView):
    """ View all recipes """
    template_name = 'recipes/recipes.html'
    model = Recipe
    context_object_name = 'recipes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'recipes'  # Pass the url_name to the context
        return context
    
    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query) |
                Q(instructions__icontains=query) |
                Q(category__icontains=query)
            )
        else:
            recipes = self.model.objects.all()
        return recipes
    
    
    
def RecipeDetails(request, slug):
    """ View Recipe details """
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)
    
    
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe})

@login_required
def like_recipe(request, slug):
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return HttpResponseRedirect(reverse('recipe_details', args=[slug]))

    

class FavoritesView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'recipes/favorites.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Assuming you have a 'likes' field in Recipe model
        # Filter recipes liked by the current user
        return Recipe.objects.filter(likes=self.request.user).order_by('-posted_on')


class MyRecipes(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'recipes/myrecipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Filter recipes posted by the current user
        return Recipe.objects.filter(author=self.request.user).order_by('-posted_on')