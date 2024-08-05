from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """ Form to create recipe """
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'image_alt', 'categories', 'calories']
        
        widgets = {
            'ingredients': forms.CheckboxSelectMultiple,
            'instructions': SummernoteWidget(),
            'categories': forms.CheckboxSelectMultiple
        }
        
        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'ingredients': 'Recipe Ingredients',
            'instructions': 'Recipe Instructions',
            'image': 'Recipe Image',
            'image_alt': 'Describe Image',
            'categories': 'Meal Categories',
        }
            
        
       