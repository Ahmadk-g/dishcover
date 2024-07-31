from django.contrib import admin
from .models import Recipe, Ingredient, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'meal_type', 'calories', 'get_ingredients')
    search_fields = ['title', 'ingredients', 'meal_type']
    list_filter = ('posted_on', 'meal_type', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('instructions', )
    # To resolves the error for including a manytomanyfield(Ingredient) in list_display
    def get_ingredients(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])

    get_ingredients.short_description = 'Ingredients'
    
admin.site.register(Ingredient)
admin.site.register(Comment)
