from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin



# Register the Recipe model
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """
    Admin view for managing Recipe model entries.
    Provides search, filter, and prepopulation functionalities.
    """
    list_display = ('title', 'category', 'calories',)
    search_fields = ['title', 'category', 'ingredients', 'description']
    list_filter = ('posted_on', 'category')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions')
