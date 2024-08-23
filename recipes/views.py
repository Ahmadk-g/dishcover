from django.contrib.auth.decorators import login_required
from typing import Any
from django.contrib import messages
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # The Add recipe view can only be accessed if the user logged in
from django.db.models import Q # a rapper for sequel queries that allows us to write complex database operations with less code
from .models import Recipe
from .forms import RecipeForm, CategoryFilterForm

# Create your views here.

class AddRecipe(LoginRequiredMixin, generic.CreateView):
    """ Add recipe view """
    template_name = 'recipes/add_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Recipe added successfully.")
        return super(AddRecipe, self).form_valid(form)
    
    def form_invalid(self, form):
        # This method is called when form validation fails
        messages.error(self.request, "There was an error creating your recipe.")
        return super().form_invalid(form)
    
    
class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView): 
    model = Recipe
    template_name = 'recipes/edit_recipe.html'
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):# For checking if the user is authorized to edit the post
        return self.request.user == self.get_object().author
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Recipe updated.")
       
        return redirect(reverse('recipe_details', kwargs={'slug': self.object.slug}))
    
    def form_invalid(self, form):
        # This method is called when form validation fails
        messages.error(self.request, "There was an error updating your recipe.")
        return super().form_invalid(form)

    

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView): # order of Arg matters 
    model = Recipe
    success_url = '/recipes/'
    #template name not required, expects the template in a certain format, ("lowercase model name"_confirm_delete)
    
    def test_func(self):# For checking if the user is authorized to delete the post
        return self.request.user == self.get_object().author
    
    def form_valid(self, form):
        messages.success(self.request, "Recipe deleted successfully.")
        
        response = super().form_valid(form) # to update the databsase
        
         # Determine the redirect URL based on the session variable
        origin_page = self.request.session.get('origin_page', 'recipes') #redirection to the right page after deleting
        if origin_page == 'my_recipes':
            return redirect(reverse_lazy('my_recipes'))
        elif origin_page =='favorites': 
            return redirect(reverse_lazy('favorites'))
        
        return response
    
    def form_invalid(self, form):
        # This method is called when form validation fails
        messages.error(self.request, "There was an error deleting your recipe.")
        return super().form_invalid(form)



class Recipes(generic.ListView):
    """ View all recipes """
    template_name = 'recipes/recipes.html'
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 8

    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['url_name'] = 'recipes'  # Pass the url_name to the context # Troubleshoot navlink.active
        context['category_filter_form'] = CategoryFilterForm(self.request.GET)  # Add the filter form to the context
        return context
    
    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        print("Selected category:", category)  # Debugging line

        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query) |
                Q(instructions__icontains=query) |
                Q(category__icontains=query)
            )
            
        elif category:
            recipes = self.model.objects.filter(category=category)
            
            
        else:
            recipes = self.model.objects.all()
            
        
        return recipes
    
    def get(self, request, *args, **kwargs): # assist in page redirection after edit or delete
        # Set the session variable based on the page the user is currently on
        request.session['origin_page'] = 'recipes'
        return super().get(request, *args, **kwargs)
    
    
    
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
        messages.success(request, "Recipe removed from favourites.")

    else:
        recipe.likes.add(request.user)
        messages.add_message(request, messages.SUCCESS, 'Recipe added to favourites!')
        # messages.success(request, "Added to favourites.")
    return HttpResponseRedirect(reverse('recipe_details', args=[slug]))

    

class FavoritesView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'recipes/favorites.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Assuming you have a 'likes' field in Recipe model
        # Filter recipes liked by the current user
        return Recipe.objects.filter(likes=self.request.user).order_by('-posted_on')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user has no favorite recipes
        if not context['recipes'].exists():
            context['no_favorites'] = True
        else:
            context['no_favorites'] = False
        return context
    
    def get(self, request, *args, **kwargs): # assist in page redirection after edit or delete
        # Set the session variable based on the page the user is currently on
        request.session['origin_page'] = 'favorites'
        return super().get(request, *args, **kwargs)


class MyRecipes(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'recipes/myrecipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Filter recipes posted by the current user
        return Recipe.objects.filter(author=self.request.user).order_by('-posted_on')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user has no favorite recipes
        if not context['recipes'].exists():
            context['no_recipes'] = True
        else:
            context['no_recipes'] = False
        return context
    
    def get(self, request, *args, **kwargs): # assist in page redirection after edit or delete
        # Set the session variable based on the page the user is currently on
        request.session['origin_page'] = 'my_recipes'
        return super().get(request, *args, **kwargs)