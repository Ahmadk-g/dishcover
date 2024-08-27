from django.contrib import admin
from .models import Recipe
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'calories',)
    search_fields = ['title', 'ingredients', 'category']
    list_filter = ('posted_on', 'category', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions')
    # To resolves the error for including a manytomanyfield(Ingredient) in list_display
