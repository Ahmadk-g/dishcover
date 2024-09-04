from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Provides messaging framework.
from django.urls import reverse, reverse_lazy  # Generate URLs by reversing URL
from django.shortcuts import render, get_object_or_404, redirect  # View tasks
from django.views import generic
from django.http import HttpResponseRedirect  # Returns an HTTP response
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q  # A rapper for sequel queries
from .models import Recipe
from .forms import RecipeForm, CategoryFilterForm

# Create your views here.


# The Add recipe view can only be accessed if the user logged in
class AddRecipe(LoginRequiredMixin, generic.CreateView):
    """
    View to allow users to add a new recipe.
    This view is only accessible to logged-in users.
    """
    template_name = 'recipes/add_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def form_valid(self, form):
        """
        Called when the submitted form is valid.
        Assigns the current user as the author of the recipe before saving.
        """
        form.instance.author = self.request.user
        messages.success(self.request, "Recipe added successfully.")
        return super(AddRecipe, self).form_valid(form)

    def form_invalid(self, form):
        """
        Called when the submitted form is invalid.
        Displays an error message to the user.
        """
        messages.error(self.request, "Recipe creation failed.")
        return super().form_invalid(form)


# Can only be accessed if the user logged in
class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    View to allow users to edit an existing recipe.
    Only the author of the recipe can edit it.
    """
    model = Recipe
    template_name = 'recipes/edit_recipe.html'
    form_class = RecipeForm
    success_url = '/recipes/'  # URL redirect after successful form submission

    def test_func(self):
        """
        Checks if the current user is the author of the recipe.
        Only the author is allowed to edit the recipe.
        """
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        """
        Called when the submitted form is valid.
        Saves the form and redirects to the recipe details page.
        """
        self.object = form.save()
        messages.success(self.request, "Recipe updated.")
        return redirect(reverse('recipe_details',
                                kwargs={'slug': self.object.slug}))

    def form_invalid(self, form):
        """
        Called when the submitted form is invalid.
        Displays an error message to the user.
        """
        messages.error(self.request, "Failed to update your recipe.")
        return super().form_invalid(form)


# Can only be accessed if the user logged in
class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    View to allow users to delete a recipe.
    Only the author of the recipe can delete it.
    """
    model = Recipe
    success_url = '/recipes/'  # URL to redirect to after successful deletion

    def test_func(self):
        """
        Checks if the current user is the author of the recipe.
        Only the author is allowed to delete the recipe.
        """
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        """
        Called when the deletion is successful.
        Redirects the user to the appropriate page
        based on the session variable.
        """
        messages.success(self.request, "Recipe deleted successfully.")
        response = super().form_valid(form)  # to update the databsase

        # Determine the redirect URL based on the session variable
        origin_page = self.request.session.get('origin_page', 'recipes')
        if origin_page == 'my_recipes':
            return redirect(reverse_lazy('my_recipes'))
        elif origin_page == 'favorites':
            return redirect(reverse_lazy('favorites'))

        return response

    def form_invalid(self, form):
        """
        Called when the deletion fails.
        Displays an error message to the user.
        """
        messages.error(self.request, "Failed to delete your recipe.")
        return super().form_invalid(form)


class Recipes(generic.ListView):
    """
    View to display a list of all recipes.
    Includes pagination and category filtering.
    """
    template_name = 'recipes/recipes.html'
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 8  # Number of recipes to display per page

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template,
        including the filter form.
        """
        context = super().get_context_data(**kwargs)
        # Pass the url_name to the context for troubleshooting active navlink
        context['url_name'] = 'recipes'
        # Add the filter form to the context
        context['category_filter_form'] = CategoryFilterForm(self.request.GET)
        return context

    def get_queryset(self, **kwargs):
        """
        Customizes the queryset based on search queries and category filters.
        """
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

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

    def get(self, request, *args, **kwargs):
        """
        Overrides the get method to set the session variable
        for page redirection after delete.
        """
        request.session['origin_page'] = 'recipes'

        return super().get(request, *args, **kwargs)


def RecipeDetails(request, slug):
    """
    View to display the details of a single recipe.
    """
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)

    return render(request, 'recipes/recipe_details.html', {'recipe': recipe})


@login_required  # Ensures the user is logged in before accessing the view.
def like_recipe(request, slug):
    """
    View to handle liking or unliking a recipe.
    """
    queryset = Recipe.objects.all()
    recipe = get_object_or_404(queryset, slug=slug)
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        messages.success(request, "Recipe removed from favourites.")

    else:
        recipe.likes.add(request.user)
        messages.success(request, "Recipe added to favourites!")

    return HttpResponseRedirect(reverse('recipe_details', args=[slug]))


# Can only be accessed if the user logged in
class FavoritesView(LoginRequiredMixin, generic.ListView):
    """
    View to display the current user's favorite recipes.
    Only accessible to logged-in users.
    """
    model = Recipe
    template_name = 'recipes/favorites.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Filter recipes liked by the current user
        return Recipe.objects.filter(likes=self.request.user).order_by('-posted_on')

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template,
        including a flag for no favorites.
        """
        context = super().get_context_data(**kwargs)
        if not context['recipes'].exists():
            context['no_favorites'] = True
        else:
            context['no_favorites'] = False
        return context

    def get(self, request, *args, **kwargs):
        """For page redirection after recipe deletipn """

        request.session['origin_page'] = 'favorites'
        return super().get(request, *args, **kwargs)


# Can only be accessed if the user logged in
class MyRecipes(LoginRequiredMixin, generic.ListView):
    """
    View to display the current user's own recipes.
    Only accessible to logged-in users.
    """
    model = Recipe
    template_name = 'recipes/myrecipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        # Filter recipes posted by the current user
        return Recipe.objects.filter(author=self.request.user).order_by('-posted_on')

    def get_context_data(self, **kwargs):
        """Check if the user has no created recipes"""

        context = super().get_context_data(**kwargs)
        if not context['recipes'].exists():
            context['no_recipes'] = True
        else:
            context['no_recipes'] = False
        return context

    def get(self, request, *args, **kwargs):
        """For page redirection after recipe deletipn """

        request.session['origin_page'] = 'my_recipes'
        return super().get(request, *args, **kwargs)
