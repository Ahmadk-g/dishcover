from django.contrib import admin
from .models import Recipe, Ingredient, Category, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'calories', 'get_ingredients', 'get_categories')
    search_fields = ['title', 'ingredients', 'categories']
    list_filter = ('posted_on', 'categories', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('instructions', )
    # To resolves the error for including a manytomanyfield(Ingredient) in list_display
    def get_ingredients(self, obj):
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    get_ingredients.short_description = 'Ingredients'
    
    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = 'Categories'
    
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Comment)
