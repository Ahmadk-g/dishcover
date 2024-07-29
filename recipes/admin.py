from django.contrib import admin
from .models import Recipe, Comment
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'posted_on', 'meal_type')
    search_fields = ['title', 'ingredients', 'meal_type']
    list_filter = ('status', 'posted_on', 'meal_type')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('ingredients', 'instructions')

admin.site.register(Comment)
