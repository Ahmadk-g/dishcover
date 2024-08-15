from django.shortcuts import render, get_object_or_404
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # The Add recipe view can only be accessed if the user logged in

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
    

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView): # order of Arg matters 
    model = Recipe
    success_url = '/recipes/'
    
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
    
    
    
def RecipeDetails(request, slug):
    """ View Recipe details """
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)
    
    
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe})
    